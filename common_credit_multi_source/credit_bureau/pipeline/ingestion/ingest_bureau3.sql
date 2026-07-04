CREATE OR REPLACE TABLE bureau3_raw (
    cust_id STRING,
    cust_name STRING,
    risk_score FLOAT,
    report_dt DATE,
    date_of_birth DATE,
    address STRING
);

COPY INTO bureau3_raw
FROM @my_s3_stage/bureau3/
FILE_FORMAT = (TYPE = PARQUET);
