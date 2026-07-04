---

## Medallion Lakehouse Architecture Design

This pipeline follows a strict **Bronze-Silver-Gold** architecture strategy to preserve data history while creating reliable end-user datasets.

* **Bronze (Raw Storage Layer)**: 
    Data drops into S3 landing zones from raw external systems in mixed formats (JSON, CSV, XML). The pipeline ingests them safely into Parquet, appending `ingested_at` processing indicators. No transformations are run here. This ensures that if a normalization rule contains an error tomorrow, we can replay historical data directly from Bronze without re-downloading source files.
    
* **Silver (Validated & Enriched Layer)**: 
    The raw data is parsed, field types are corrected, and schemas are standardized into an identical tabular shape across all bureaus. Invalid records (missing critical items like National IDs) are caught and flagged during metrics collection. Credit score metrics are normalized mathematically to a standard 300–850 threshold.
    
* **Gold (Business Analytics Layer)**: 
    Data from all bureaus is unioned together. A final Spark SQL processing step performs identity resolution by grouping on `national_id`. This creates a consolidated profile showcasing global loan statistics, a blended risk score, and an array lineage of which systems originally provided the records. Downstream production services or credit officers only ever query this optimized Gold table.