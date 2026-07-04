CREATE OR REPLACE VIEW bureau1_normalized AS
SELECT
    applicant_id,
    full_name AS name,
    (score::FLOAT) / 850.0 AS normalized_score,
    report_date,
    'bureau1' AS source
FROM bureau1_raw;
