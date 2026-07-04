CREATE OR REPLACE VIEW bureau2_normalized AS
SELECT
    id AS applicant_id,
    name,
    (credit_rating::FLOAT) / 100.0 AS normalized_score,
    date_reported AS report_date,
    date_of_birth,
    address,
    'bureau2' AS source
FROM bureau2_raw;
