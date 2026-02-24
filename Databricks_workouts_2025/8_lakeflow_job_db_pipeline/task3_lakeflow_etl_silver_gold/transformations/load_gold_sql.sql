CREATE OR REFRESH MATERIALIZED VIEW catalog.schema.gold_shipments_agg
AS
SELECT
  role,avg(age) avgage,count(1) cnt
FROM
  catalog3_we47.schema3_we47.silver_shipments
  GROUP BY
    role;