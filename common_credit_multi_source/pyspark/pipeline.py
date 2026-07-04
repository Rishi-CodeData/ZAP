import yaml
import sys
from pyspark.sql import SparkSession
from pyspark.sql import functions as F
from parser import BureauParser  # Keeps the same mapping logic from previous answer

def load_config(config_path):
    with open(config_path, 'r') as file:
        return yaml.safe_load(file)

def main():
    spark = SparkSession.builder \
        .appName("BureauMedallionPipeline") \
        .config("spark.sql.sources.commitProtocolClass", "org.apache.spark.internal.io.HadoopMapReduceCommitProtocol") \
        .getOrCreate()

    config = load_config("config/pipeline_config.yaml")
    parser = BureauParser(spark)
    
    layers = config['lakehouse_layers']
    reconciliation_data = []
    silver_dfs = []

    # ==========================================
    # 1. BRONZE LAYER: Ingestion & Cold Storage
    # ==========================================
    for bureau, meta in config['sources'].items():
        try:
            landing_path = meta['s3_raw_landing']
            fmt = meta['format']
            options = meta.get('options', {})

            # Read exact raw data from S3 landing zone
            raw_landing_df = spark.read.format(fmt).options(**options).load(landing_path)
            
            # Append execution metadata for historical audit tracking
            bronze_df = raw_landing_df.withColumn("ingested_at", F.current_timestamp()) \
                                      .withColumn("source_file_name", F.input_file_name())

            # Save directly to Bronze with zero structure modifications
            bronze_target = f"{layers['bronze_path']}{bureau}/"
            bronze_df.write.mode("overwrite").parquet(bronze_target)
            
            # ==========================================
            # 2. SILVER LAYER: Cleaning & Normalization
            # ==========================================
            # Read straight back out of Bronze to preserve lineage
            bronze_source_df = spark.read.parquet(bronze_target)
            total_inbound = bronze_source_df.count()

            # Execute normalization transformations mapped in parser.py
            parser_func = getattr(parser, f"parse_{bureau}")
            normalized_df = parser_func(bronze_source_df)

            # Filter data quality rules (Check if core key metrics exist)
            incomplete_df = normalized_df.filter(
                F.col("national_id").isNull() | F.col("normalized_score").isNull()
            )
            incomplete_count = incomplete_df.count()
            matched_count = total_inbound - incomplete_count

            # Extract clean records
            clean_silver_df = normalized_df.filter(F.col("national_id").isNotNull())
            
            # Write out individual clean Silver tables
            silver_target = f"{layers['silver_path']}{bureau}/"
            clean_silver_df.write.mode("overwrite").parquet(silver_target)
            
            # Collect paths for Gold processing
            silver_dfs.append(spark.read.parquet(silver_target))

            # Store metrics for reporting
            reconciliation_data.append((bureau, total_inbound, matched_count, incomplete_count))

        except Exception as e:
            print(f"Error executing processing layer for {bureau}: {str(e)}")
            continue

    if not silver_dfs:
        print("No active datasets compiled into Silver. Shutting down execution.")
        sys.exit(0)

    # ==========================================
    # 3. GOLD LAYER: Aggregation & Business Views
    # ==========================================
    # Merge all individual silver outputs into a single consolidated view
    unified_silver_df = silver_dfs[0]
    for df in silver_dfs[1:]:
        unified_silver_df = unified_silver_df.unionByName(df)

    # Register Spark SQL View to aggregate cross-bureau realities
    unified_silver_df.createOrReplaceTempView("silver_normalized_reports")

    # Combine profiles sharing the same identity (National ID)
    gold_profile_df = spark.sql("""
        SELECT 
            national_id,
            MAX(first_name) AS first_name,
            MAX(last_name) AS last_name,
            
            -- Blend metrics across multiple reporting bureaus safely
            ROUND(AVG(normalized_score), 2) AS blended_credit_score,
            SUM(active_loans_count) AS aggregate_active_loans,
            SUM(total_overdue_amount) AS total_outstanding_delinquency,
            
            -- Keep audit trail of which bureaus contributed data to this profile
            COLLECT_SET(bureau_source) AS contributing_bureaus,
            CURRENT_TIMESTAMP() AS updated_at
        FROM silver_normalized_reports
        GROUP BY national_id
    """)

    # Write final single-source-of-truth table to Gold
    gold_profile_df.write.mode("overwrite").parquet(f"{layers['gold_path']}unified_applicant_profile/")

    # ==========================================
    # 4. RECONCILIATION SUMMARY OUTPUT
    # ==========================================
    recon_schema = ["bureau_name", "bronze_inbound_count", "silver_clean_count", "quarantined_incomplete_count"]
    recon_df = spark.createDataFrame(reconciliation_data, schema=recon_schema)
    recon_df.write.mode("overwrite").json(f"{layers['gold_path']}reconciliation_summary/")

    print("Medallion execution completed successfully.")
    spark.stop()

if __name__ == "__main__":
    main()