-- This file defines a sample transformation.
-- Edit the sample below or add new transformations
-- using "+ Add" in the file browser.

CREATE MATERIALIZED VIEW sample_aggregation_first_lakeflow_etl_declarative_dlt_pipeline_wd36 AS
SELECT
    user_type,
    COUNT(user_type) AS total_count
FROM sample_users_first_lakeflow_etl_declarative_dlt_pipeline_wd36
GROUP BY user_type;
