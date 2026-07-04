CREATE OR REPLACE VIEW bureau3_normalized AS
SELECT
    cust_id AS applicant_id,
    cust_name AS name,
    risk_score,
    report_dt AS report_date,
    date_of_birth,
    address,
    'bureau3' AS source
FROM bureau3_raw;
