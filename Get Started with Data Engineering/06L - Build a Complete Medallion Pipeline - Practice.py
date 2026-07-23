# Databricks notebook source
# MAGIC %md-sandbox
# MAGIC
# MAGIC <div style="max-width: 1000px; margin: 0 auto; font-family: sans-serif;">
# MAGIC
# MAGIC <div style="background: #02A36F; color: white; border-radius: 8px; padding: 28px 32px; text-align: center; position: relative;">
# MAGIC   <div style="font-size: 14pt; font-weight: 600; text-transform: uppercase; letter-spacing: 1px; opacity: 0.85; margin-bottom: 8px;">Practice</div>
# MAGIC   <div style="font-size: 24pt; font-weight: 700; line-height: 1.3;">Build a Complete Medallion Pipeline</div>
# MAGIC   <div style="font-size: 14pt; margin-top: 12px; opacity: 0.9;">Build your own Bronze, Silver, and Gold tables with different transformations and a different aggregation.</div>
# MAGIC </div>
# MAGIC
# MAGIC </div>

# COMMAND ----------


# MAGIC %md
# MAGIC ### Instructions
# MAGIC
# MAGIC In Lesson 6, you built a full Medallion pipeline where Silver uppercased the `Role` column and Gold counted employees by role. Now you'll build your own pipeline with different transformations:
# MAGIC - **Bronze:** Same raw ingestion from CSV files
# MAGIC - **Silver:** Uppercase the `Country` column (not Role) and add a row number
# MAGIC - **Gold:** Count employees by **country** instead of by role
# MAGIC
# MAGIC Your goal: create **`practice_bronze`**, **`practice_silver`**, and **`country_count_gold`** tables.

# COMMAND ----------

# MAGIC %md
# MAGIC ---
# MAGIC ## Part 1: Bronze and Silver

# COMMAND ----------

# MAGIC %md
# MAGIC ### Task 1: Create a Bronze table
# MAGIC
# MAGIC Create an empty table called `practice_bronze` with columns: `ID` (INT), `FirstName` (STRING), `Country` (STRING), `Role` (STRING). Then load all CSV files from the volume using COPY INTO.

# COMMAND ----------

# MAGIC %sql
# MAGIC USE CATALOG dbacademy;
# MAGIC USE SCHEMA get_started_de;
# MAGIC
# MAGIC -- TODO: Create the empty practice_bronze table
# MAGIC <FILL_IN>

# COMMAND ----------

# MAGIC %md-sandbox
# MAGIC <details>
# MAGIC <summary>Hint</summary>
# MAGIC
# MAGIC <pre><code>CREATE TABLE IF NOT EXISTS practice_bronze (
# MAGIC   ID INT,
# MAGIC   FirstName STRING,
# MAGIC   Country STRING,
# MAGIC   Role STRING
# MAGIC );</code></pre>
# MAGIC
# MAGIC </details>

# COMMAND ----------

# TODO: Load data into practice_bronze with COPY INTO
result = spark.sql("""
    COPY INTO <FILL_IN>
    FROM '<FILL_IN>'
    FILEFORMAT = CSV
    FORMAT_OPTIONS ('header' = 'true', 'inferSchema' = 'true')
""")
result.display()

# COMMAND ----------

# MAGIC %md-sandbox
# MAGIC <details>
# MAGIC <summary>Hint</summary>
# MAGIC
# MAGIC <pre><code>result = spark.sql("""
# MAGIC     COPY INTO practice_bronze
# MAGIC     FROM '/Volumes/dbacademy/get_started_de/myfiles/'
# MAGIC     FILEFORMAT = CSV
# MAGIC     FORMAT_OPTIONS ('header' = 'true', 'inferSchema' = 'true')
# MAGIC """)
# MAGIC result.display()</code></pre>
# MAGIC
# MAGIC </details>

# COMMAND ----------

# MAGIC %md
# MAGIC Verify Bronze has 6 rows.

# COMMAND ----------

# MAGIC %sql
# MAGIC SELECT * FROM practice_bronze;

# COMMAND ----------

# MAGIC %md
# MAGIC ### Task 2: Create a Silver table with transformations
# MAGIC
# MAGIC Create `practice_silver` from `practice_bronze` with these transformations:
# MAGIC - Uppercase the **Country** column (not Role this time)
# MAGIC - Add a **processed_timestamp** column using `current_timestamp()`
# MAGIC - Add a **row_number** column using the `ROW_NUMBER()` window function ordered by ID

# COMMAND ----------

# MAGIC %sql
# MAGIC -- TODO: Create practice_silver with the transformations described above
# MAGIC <FILL_IN>

# COMMAND ----------

# MAGIC %md-sandbox
# MAGIC <details>
# MAGIC <summary>Hint</summary>
# MAGIC
# MAGIC <pre><code>CREATE OR REPLACE TABLE practice_silver AS
# MAGIC SELECT
# MAGIC   ID,
# MAGIC   FirstName,
# MAGIC   UPPER(Country) AS Country,
# MAGIC   Role,
# MAGIC   current_timestamp() AS processed_timestamp,
# MAGIC   ROW_NUMBER() OVER (ORDER BY ID) AS row_number
# MAGIC FROM practice_bronze;</code></pre>
# MAGIC
# MAGIC </details>

# COMMAND ----------

# MAGIC %md
# MAGIC ### Task 3: Verify your Silver table

# COMMAND ----------

# MAGIC %sql
# MAGIC -- TODO: Query practice_silver
# MAGIC <FILL_IN>

# COMMAND ----------

# MAGIC %md-sandbox
# MAGIC <details>
# MAGIC <summary>Hint</summary>
# MAGIC
# MAGIC <pre><code>SELECT * FROM practice_silver;</code></pre>
# MAGIC
# MAGIC </details>

# COMMAND ----------

# MAGIC %md
# MAGIC You should see 6 rows with:
# MAGIC - **Country** in uppercase (e.g., `UNITED STATES` instead of `United States`)
# MAGIC - A **processed_timestamp** showing when the transformation ran
# MAGIC - A **row_number** from 1 to 6

# COMMAND ----------

# MAGIC %md
# MAGIC ### Task 4: Compare Bronze and Silver
# MAGIC
# MAGIC Run the query below to see the column differences between your Bronze and Silver tables.

# COMMAND ----------

# MAGIC %sql
# MAGIC SELECT 'practice_bronze' AS table_name, COUNT(*) AS column_count
# MAGIC FROM information_schema.columns
# MAGIC WHERE table_schema = 'get_started_de' AND table_name = 'practice_bronze'
# MAGIC UNION ALL
# MAGIC SELECT 'practice_silver', COUNT(*)
# MAGIC FROM information_schema.columns
# MAGIC WHERE table_schema = 'get_started_de' AND table_name = 'practice_silver';

# COMMAND ----------

# MAGIC %md
# MAGIC Bronze has **4 columns** (raw data). Silver has **6 columns** (added `processed_timestamp` and `row_number`). The transformation added structure and audit information on top of the raw data.

# COMMAND ----------

# MAGIC %md
# MAGIC ---
# MAGIC ## Part 2: Gold and Governance

# COMMAND ----------

# MAGIC %md
# MAGIC ### Task 5: Create a temp view for the aggregation
# MAGIC
# MAGIC Create a temp view called `temp_country_counts` that counts employees by `Country` from `practice_silver`.

# COMMAND ----------

# MAGIC %sql
# MAGIC -- TODO: Create a temp view that counts employees by Country
# MAGIC <FILL_IN>

# COMMAND ----------

# MAGIC %md-sandbox
# MAGIC <details>
# MAGIC <summary>Hint</summary>
# MAGIC
# MAGIC <pre><code>CREATE OR REPLACE TEMP VIEW temp_country_counts AS
# MAGIC SELECT
# MAGIC   Country,
# MAGIC   COUNT(*) AS TotalEmployees
# MAGIC FROM practice_silver
# MAGIC GROUP BY Country;</code></pre>
# MAGIC
# MAGIC </details>

# COMMAND ----------

# MAGIC %md
# MAGIC Verify the aggregation looks right.

# COMMAND ----------

# MAGIC %sql
# MAGIC SELECT * FROM temp_country_counts;

# COMMAND ----------

# MAGIC %md
# MAGIC ### Task 6: Create the Gold table and load it
# MAGIC
# MAGIC Create a table called `country_count_gold` with columns `Country` (STRING) and `TotalEmployees` (INT), then use `INSERT OVERWRITE` to populate it from your temp view.

# COMMAND ----------

# MAGIC %sql
# MAGIC -- TODO: Create the Gold table and load it
# MAGIC <FILL_IN>

# COMMAND ----------

# MAGIC %md-sandbox
# MAGIC <details>
# MAGIC <summary>Hint</summary>
# MAGIC
# MAGIC <pre><code>CREATE TABLE IF NOT EXISTS country_count_gold (
# MAGIC   Country STRING,
# MAGIC   TotalEmployees INT
# MAGIC );
# MAGIC
# MAGIC INSERT OVERWRITE country_count_gold
# MAGIC SELECT * FROM temp_country_counts;</code></pre>
# MAGIC
# MAGIC </details>

# COMMAND ----------

# MAGIC %md
# MAGIC ### Task 7: Query the Gold table

# COMMAND ----------

# MAGIC %sql
# MAGIC -- TODO: Query country_count_gold
# MAGIC <FILL_IN>

# COMMAND ----------

# MAGIC %md-sandbox
# MAGIC <details>
# MAGIC <summary>Hint</summary>
# MAGIC
# MAGIC <pre><code>SELECT * FROM country_count_gold;</code></pre>
# MAGIC
# MAGIC </details>

# COMMAND ----------

# MAGIC %md
# MAGIC You should see one row per country with the count of employees from each. This answers a different business question than the lesson's Gold table, but both are sourced from the same Silver layer pattern.

# COMMAND ----------

# MAGIC %md
# MAGIC ### Task 8: Explore governance
# MAGIC
# MAGIC Open Catalog Explorer and navigate to `country_count_gold`. Check the **Lineage** tab to see if you can trace it back to `practice_silver` and `practice_bronze`.

# COMMAND ----------

# MAGIC %md-sandbox
# MAGIC
# MAGIC <div style="max-width: 900px; margin: 0 auto; font-family: sans-serif;">
# MAGIC <div style="margin-top: 10px; padding: 18px 24px; background: #FFF6F4; border: 3px solid #FF5F46; border-radius: 10px;">
# MAGIC   <div style="font-size: 14pt; color: #0b2026; line-height: 1.6;">
# MAGIC     <div style="font-weight: 700; margin-bottom: 8px;">Nice work! You just:</div>
# MAGIC     <ul style="padding-left: 20px; margin: 0;">
# MAGIC       <li>Built a Bronze table with raw data using <code>COPY INTO</code></li>
# MAGIC       <li>Transformed it into a Silver table with <code>UPPER()</code>, timestamps, and <code>ROW_NUMBER()</code></li>
# MAGIC       <li>Created a Gold aggregation table counting employees by country</li>
# MAGIC       <li>Used the <code>INSERT OVERWRITE</code> pattern for refreshable Gold tables</li>
# MAGIC       <li>Explored lineage to trace data from Bronze through Silver to Gold</li>
# MAGIC     </ul>
# MAGIC   </div>
# MAGIC </div>
# MAGIC </div>

# COMMAND ----------

# MAGIC %md-sandbox
# MAGIC
# MAGIC <!-- CHECKPOINT: Lesson 6 -->
# MAGIC
# MAGIC <div style="max-width: 900px; margin: 0 auto; font-family: sans-serif;">
# MAGIC
# MAGIC <div style="background: #1B5162; color: white; border-radius: 8px; padding: 24px 28px; text-align: center;">
# MAGIC   <div style="font-size: 14pt; font-weight: 600; text-transform: uppercase; letter-spacing: 1px; opacity: 0.85; margin-bottom: 8px;">Checkpoint</div>
# MAGIC   <div style="font-size: 20pt; font-weight: 700;">What You've Done So Far</div>
# MAGIC </div>
# MAGIC
# MAGIC <div style="margin-top: 16px; padding: 20px 24px; background: #F9F7F4; border-radius: 8px; box-shadow: 0 2px 8px rgba(27,49,57,0.06);">
# MAGIC   <div style="font-size: 14pt; color: #0b2026; line-height: 1.7;">
# MAGIC     <p>Over Lessons 1 through 6, you:</p>
# MAGIC     <ul style="padding-left: 20px; margin: 8px 0;">
# MAGIC       <li>Navigated Unity Catalog and worked with volumes, schemas, and tables</li>
# MAGIC       <li>Created Delta tables from CSV files using multiple ingestion methods</li>
# MAGIC       <li>Modified data with DML and explored version history with time travel</li>
# MAGIC       <li>Built a complete Medallion Architecture pipeline (Bronze → Silver → Gold)</li>
# MAGIC       <li>Explored governance features: lineage, permissions, and insights</li>
# MAGIC     </ul>
# MAGIC   </div>
# MAGIC </div>
# MAGIC
# MAGIC <div style="margin-top: 16px; padding: 16px 20px; background: #F8F9FC; border-left: 4px solid #1B5162; border-radius: 6px;">
# MAGIC   <div style="font-size: 14pt; color: #0b2026; line-height: 1.6;">
# MAGIC     <strong>Quick self-check:</strong> Could you explain to a teammate why data goes through three layers instead of loading it straight into a final table?
# MAGIC   </div>
# MAGIC </div>
# MAGIC
