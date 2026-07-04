CREATE OR REPLACE VIEW unified_applicants AS
SELECT applicant_id, name, normalized_score, report_date, date_of_birth, address, source
FROM bureau1_normalized
UNION ALL
SELECT applicant_id, name, normalized_score, report_date, date_of_birth, address, source
FROM bureau2_normalized
UNION ALL
SELECT applicant_id, name, normalized_score, report_date, date_of_birth, address, source
FROM bureau3_normalized;
