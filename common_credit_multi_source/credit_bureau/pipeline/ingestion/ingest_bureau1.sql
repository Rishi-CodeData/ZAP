CREATE OR REPLACE TABLE bureau1_raw (
    applicant_id STRING,
    full_name STRING,
    score INT,
    report_date DATE,
    date_of_birth DATE,
    address STRING
);

COPY INTO bureau1_raw
FROM @my_s3_stage/bureau1/bureau1.csv
FILE_FORMAT = (TYPE = CSV FIELD_OPTIONALLY_ENCLOSED_BY='"' SKIP_HEADER=1);
