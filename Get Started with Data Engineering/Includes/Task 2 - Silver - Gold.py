# Databricks notebook source
# MAGIC %md
# MAGIC # Task 2: Silver and Gold Layers
# MAGIC This notebook is used as a task in a LakeFlow Job. It transforms Bronze into Silver and aggregates into Gold.

# COMMAND ----------

# Set catalog and schema
spark.sql("USE CATALOG dbacademy")
spark.sql("USE SCHEMA get_started_de")

# COMMAND ----------

# Create Silver table from Bronze
spark.sql("""
    CREATE OR REPLACE TABLE current_employees_silver_job AS
    SELECT
        ID,
        FirstName,
        Country,
        UPPER(Role) AS Role,
        current_timestamp() AS processed_timestamp,
        current_date() AS processed_date
    FROM current_employees_bronze_job
""")

print("Silver table created")
display(spark.sql("SELECT * FROM current_employees_silver_job"))

# COMMAND ----------

# Create Gold table from Silver
spark.sql("""
    CREATE TABLE IF NOT EXISTS total_roles_gold_job (
        Role STRING,
        TotalEmployees INT
    )
""")

spark.sql("""
    INSERT OVERWRITE total_roles_gold_job
    SELECT Role, COUNT(*) AS TotalEmployees
    FROM current_employees_silver_job
    GROUP BY Role
""")

print("Gold table created")
display(spark.sql("SELECT * FROM total_roles_gold_job"))

