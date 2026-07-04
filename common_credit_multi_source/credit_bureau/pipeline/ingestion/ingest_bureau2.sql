CREATE OR REPLACE TABLE bureau2_raw (
    id STRING,
    name STRING,
    credit_rating INT,
    date_reported DATE
);

COPY INTO bureau2_raw
FROM @my_s3_stage/bureau2/bureau2.json
FILE_FORMAT = (TYPE = JSON);
