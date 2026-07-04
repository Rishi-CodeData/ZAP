CREATE OR REPLACE VIEW reconciliation_summary AS
SELECT
    name,
    COUNT(DISTINCT source) AS bureau_count,
    MIN(normalized_score) AS min_score,
    MAX(normalized_score) AS max_score,
    CASE
        WHEN COUNT(DISTINCT source) = 3 THEN 'complete'
        WHEN COUNT(DISTINCT source) = 2 THEN 'partial'
        ELSE 'incomplete'
    END AS status
FROM unified_applicants
GROUP BY name;
