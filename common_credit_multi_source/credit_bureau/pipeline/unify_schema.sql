CREATE OR REPLACE VIEW unified_applicants AS
SELECT * FROM bureau1_normalized
UNION ALL
SELECT * FROM bureau2_normalized
UNION ALL
SELECT * FROM bureau3_normalized;
