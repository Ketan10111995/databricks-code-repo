-- This file defines a sample transformation.
-- Edit the sample below or add new transformations
-- using "+ Add" in the file browser.

CREATE OR REFRESH MATERIALIZED VIEW sample_users_first_lakeflow_etl_declarative_dlt_pipeline_wd36 AS
SELECT
    user_id,
    email,
    name,
    user_type
FROM samples.wanderbricks.users;
