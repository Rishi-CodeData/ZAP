# Credit Bureau Normalization Pipeline (Snowflake)

## Overview
This pipeline ingests credit bureau reports from S3 into Snowflake, normalizes them into a unified schema, and produces a reconciliation summary.

## How to Run
1. Clone repo
2. Configure Snowflake stage pointing to your S3 bucket:
   ```sql
   CREATE STAGE my_s3_stage
   URL='s3://credit-bureau-data/'
   STORAGE_INTEGRATION = my_integration;
