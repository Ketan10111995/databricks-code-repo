# Databricks notebook source
# MAGIC %md-sandbox
# MAGIC
# MAGIC <div style="max-width: 1000px; margin: 0 auto; font-family: sans-serif;">
# MAGIC
# MAGIC <div style="background: #1B5162; color: white; border-radius: 8px; padding: 28px 32px; text-align: center; position: relative;">
# MAGIC   <div style="font-size: 14pt; font-weight: 600; text-transform: uppercase; letter-spacing: 1px; opacity: 0.85; margin-bottom: 8px;">Lesson 6</div>
# MAGIC   <div style="font-size: 24pt; font-weight: 700; line-height: 1.3;">Build a Medallion Architecture Pipeline</div>
# MAGIC   <div style="font-size: 14pt; margin-top: 12px; opacity: 0.9;">Ingest raw data into Bronze, transform it into Silver, aggregate it into Gold, and explore how Databricks tracks the full pipeline.</div>
# MAGIC </div>
# MAGIC
# MAGIC </div>

# COMMAND ----------


# MAGIC %md
# MAGIC **In this lesson:** You'll organize the process of getting data into tables into a production pattern.

# COMMAND ----------

# MAGIC %md-sandbox
# MAGIC
# MAGIC <!-- LEARN: Medallion Architecture -->
# MAGIC <!-- Template: vertical-layered-stack (3 layers) -->
# MAGIC
# MAGIC <div style="max-width: 900px; margin: 0 auto; font-family: sans-serif;">
# MAGIC
# MAGIC <div style="font-size: 20pt; font-weight: 700; color: #0b2026; margin-bottom: 6px;">The Medallion Architecture</div>
# MAGIC <div style="font-size: 14pt; color: #5A6F77; margin-bottom: 24px;">The Medallion Architecture organizes data into three layers. Each layer adds quality and structure, moving data from raw ingestion to business-ready analytics.</div>
# MAGIC
# MAGIC <div style="display: flex; align-items: stretch; gap: 16px;">
# MAGIC
# MAGIC <!-- Left arrow label -->
# MAGIC <div style="
# MAGIC     writing-mode: vertical-lr;
# MAGIC     transform: rotate(180deg);
# MAGIC     text-align: center;
# MAGIC     font-weight: 700;
# MAGIC     font-size: 14pt;
# MAGIC     color: #618794;
# MAGIC     padding: 0 6px;
# MAGIC     display: flex;
# MAGIC     justify-content: flex-end;
# MAGIC ">
# MAGIC &larr; RAW TO REFINED
# MAGIC </div>
# MAGIC
# MAGIC <!-- Stacked layers -->
# MAGIC <div style="flex: 1; display: flex; flex-direction: column; gap: 6px;">
# MAGIC
# MAGIC <!-- Bronze -->
# MAGIC <div style="background: #CD7F32; color: white; border-radius: 8px 8px 4px 4px; padding: 22px 24px; text-align: center;">
# MAGIC   <div style="font-size: 18pt; font-weight: 700;">Bronze — Raw Ingestion</div>
# MAGIC   <div style="font-size: 14pt; margin-top: 6px; opacity: 0.9;">Data exactly as it arrived. No transformations, no filtering. The source of truth for what was received.</div>
# MAGIC </div>
# MAGIC
# MAGIC <!-- Silver -->
# MAGIC <div style="background: #90A5B1; color: white; border-radius: 4px; padding: 18px 24px; text-align: center;">
# MAGIC   <div style="font-size: 16pt; font-weight: 700;">Silver — Cleaned &amp; Enriched</div>
# MAGIC   <div style="font-size: 14pt; margin-top: 6px; opacity: 0.9;">Data is cleaned, standardized, and enriched. Duplicates removed, types corrected, audit columns added. The foundation for analysis.</div>
# MAGIC </div>
# MAGIC
# MAGIC <!-- Gold -->
# MAGIC <div style="background: #FFAB00; color: #0b2026; border-radius: 4px 4px 8px 8px; padding: 18px 24px; text-align: center;">
# MAGIC   <div style="font-size: 16pt; font-weight: 700;">Gold — Business-Ready</div>
# MAGIC   <div style="font-size: 14pt; margin-top: 6px; opacity: 0.85;">Aggregated, filtered, or joined for specific business use cases. What dashboards and analysts consume.</div>
# MAGIC </div>
# MAGIC
# MAGIC </div>
# MAGIC
# MAGIC </div>
# MAGIC
# MAGIC <!-- Key point callout -->
# MAGIC <div style="margin-top: 20px; padding: 16px 20px; background: #FFF6F4; border: 3px solid #FF5F46; border-radius: 10px;">
# MAGIC   <div style="font-size: 14pt; color: #0b2026; line-height: 1.6;">
# MAGIC     <strong>Why three layers?</strong> Keeping raw data separate from cleaned data means you can always go back to the source. If a transformation has a bug, you fix the Silver logic and re-run it from Bronze. You never lose the original data.
# MAGIC   </div>
# MAGIC </div>
# MAGIC
# MAGIC </div>
# MAGIC
# MAGIC <div style="max-width: 900px; margin: 0 auto; font-family: sans-serif;">
# MAGIC
# MAGIC ##### EXPAND FOR ADDITIONAL NOTES
# MAGIC
# MAGIC <details>
# MAGIC
# MAGIC **The Medallion Architecture in practice**
# MAGIC
# MAGIC - **Bronze** is your landing zone. Data arrives from files, APIs, streaming sources, or partner feeds and lands here with no changes. Even if the data has quality issues (missing values, wrong types, duplicates), it all goes into Bronze as-is.
# MAGIC - **Silver** is where you apply business rules. Standardize column names, cast data types, remove duplicates, add audit timestamps, filter out invalid records. This is the layer most data engineers spend their time building.
# MAGIC - **Gold** is purpose-built for consumers. A Gold table might aggregate daily revenue by region for a finance dashboard, or join customer and order data for a marketing report. You often have multiple Gold tables sourced from the same Silver tables.
# MAGIC - The architecture is not rigid. Some teams add a "Platinum" layer for ML features. Others skip Gold and let analysts query Silver directly. The core principle is the same: separate raw ingestion from transformation from consumption.
# MAGIC
# MAGIC </details>
# MAGIC
# MAGIC </div>

# COMMAND ----------

# MAGIC %md
# MAGIC ### Explore: Build the Bronze layer
# MAGIC
# MAGIC First, let's confirm what files are available in the volume.

# COMMAND ----------

# MAGIC %sql
# MAGIC USE CATALOG dbacademy;
# MAGIC USE SCHEMA get_started_de;
# MAGIC
# MAGIC LIST '/Volumes/dbacademy/get_started_de/myfiles/';

# COMMAND ----------

# MAGIC %md
# MAGIC Now create a Bronze table and load all CSV files into it using COPY INTO. Bronze is raw data — no transformations.

# COMMAND ----------

# MAGIC %sql
# MAGIC CREATE TABLE IF NOT EXISTS current_employees_bronze (
# MAGIC   ID INT,
# MAGIC   FirstName STRING,
# MAGIC   Country STRING,
# MAGIC   Role STRING
# MAGIC );

# COMMAND ----------

result = spark.sql("""
    COPY INTO current_employees_bronze
    FROM '/Volumes/dbacademy/get_started_de/myfiles/'
    FILEFORMAT = CSV
    FORMAT_OPTIONS ('header' = 'true', 'inferSchema' = 'true')
""")
result.display()

# COMMAND ----------

# MAGIC %sql
# MAGIC SELECT * FROM current_employees_bronze;

# COMMAND ----------

# MAGIC %md
# MAGIC You should see **6 rows** — all employees from both CSV files, loaded as-is. This is your Bronze table: raw, unmodified data.

# COMMAND ----------

# MAGIC %md
# MAGIC ### Explore: Build the Silver layer
# MAGIC
# MAGIC Now transform the Bronze data into a cleaned Silver table. We'll standardize the `Role` column to uppercase and add audit timestamps so you know when each record was processed.

# COMMAND ----------

# MAGIC %sql
# MAGIC CREATE OR REPLACE TABLE current_employees_silver AS
# MAGIC SELECT
# MAGIC   ID,
# MAGIC   FirstName,
# MAGIC   Country,
# MAGIC   UPPER(Role) AS Role,
# MAGIC   current_timestamp() AS processed_timestamp,
# MAGIC   current_date() AS processed_date
# MAGIC FROM current_employees_bronze;

# COMMAND ----------

# MAGIC %sql
# MAGIC SELECT * FROM current_employees_silver;

# COMMAND ----------

# MAGIC %md
# MAGIC Compare Silver to Bronze:
# MAGIC - **Role** is now uppercase (`Data Engineer` → `DATA ENGINEER`)
# MAGIC - Two new columns: **processed_timestamp** and **processed_date** — audit trail showing when the transformation ran
# MAGIC - Same 6 rows, but now cleaned and enriched
# MAGIC
# MAGIC Silver is where most analysis starts. Bronze is your backup if you ever need to re-process from the original data.

# COMMAND ----------

# MAGIC %md
# MAGIC ---
# MAGIC ### Explore: Build the Gold layer
# MAGIC
# MAGIC Gold tables are what analysts and dashboards consume — aggregated, business-ready data built to answer a specific question.
# MAGIC
# MAGIC Before writing the Gold table, let's define the aggregation logic in a temporary view. This counts employees by role.

# COMMAND ----------

# MAGIC %sql
# MAGIC CREATE OR REPLACE TEMP VIEW temp_total_roles AS
# MAGIC SELECT
# MAGIC   Role,
# MAGIC   COUNT(*) AS TotalEmployees
# MAGIC FROM current_employees_silver
# MAGIC GROUP BY Role;

# COMMAND ----------

# MAGIC %sql
# MAGIC SELECT * FROM temp_total_roles;

# COMMAND ----------

# MAGIC %md
# MAGIC The temp view shows the count of employees for each role. Now let's write this into a Gold table.

# COMMAND ----------

# MAGIC %sql
# MAGIC CREATE TABLE IF NOT EXISTS total_roles_gold (
# MAGIC   Role STRING,
# MAGIC   TotalEmployees INT
# MAGIC );

# COMMAND ----------

# MAGIC %sql
# MAGIC INSERT OVERWRITE total_roles_gold
# MAGIC SELECT * FROM temp_total_roles;

# COMMAND ----------

# MAGIC %sql
# MAGIC SELECT * FROM total_roles_gold;

# COMMAND ----------

# MAGIC %md
# MAGIC You now have a Gold table that answers a specific business question: "How many employees do we have in each role?" This is what a dashboard or report would query.
# MAGIC
# MAGIC The `INSERT OVERWRITE` pattern means you can refresh this table by re-running the same command. It replaces the data completely with the latest aggregation from Silver.

# COMMAND ----------

# MAGIC %md
# MAGIC ### Explore: Check the version history

# COMMAND ----------

# MAGIC %sql
# MAGIC DESCRIBE HISTORY total_roles_gold;

# COMMAND ----------

# MAGIC %md
# MAGIC ---
# MAGIC ### Explore: View lineage and governance in Catalog Explorer
# MAGIC
# MAGIC Now that you've built the full pipeline, let's see how Databricks tracks it automatically.
# MAGIC
# MAGIC **Follow these steps:**
# MAGIC
# MAGIC 1. In the left sidebar, click **Catalog**
# MAGIC 2. Navigate to `dbacademy` → `get_started_de` → **Tables** → `total_roles_gold`
# MAGIC 3. Click the **Lineage** tab → click **See lineage graph**
# MAGIC    - You should see the chain: CSV files → Bronze → Silver → Gold
# MAGIC 4. Click the **Permissions** tab
# MAGIC    - Click **Grant** to see the available permission options, then click **Cancel**
# MAGIC    - In production, this is how you'd control who can query each table
# MAGIC 5. Click the **Insights** tab
# MAGIC    - This shows recent query activity on the table
# MAGIC    - In a production environment, this helps you understand which tables are actively being used
# MAGIC
# MAGIC *Note: Lineage data may take a few minutes to appear. If the lineage graph isn't visible yet, check back shortly.*

# COMMAND ----------

# MAGIC %md-sandbox
# MAGIC
# MAGIC <div style="max-width: 900px; margin: 0 auto; font-family: sans-serif;">
# MAGIC
# MAGIC ##### EXPAND FOR ADDITIONAL NOTES
# MAGIC
# MAGIC <details>
# MAGIC
# MAGIC **Gold tables in practice**
# MAGIC
# MAGIC - Gold tables are purpose-built. While Bronze and Silver are shared infrastructure, Gold tables are often built for a specific team, dashboard, or report.
# MAGIC - A common pattern is using `INSERT OVERWRITE` instead of `CREATE OR REPLACE`. This lets you define the Gold table once (with the right schema and permissions) and then refresh its contents on a schedule without recreating the table.
# MAGIC - You might have multiple Gold tables sourced from the same Silver table: one for finance (revenue aggregations), one for HR (headcount by department), one for ops (SLA metrics).
# MAGIC
# MAGIC **Data governance features**
# MAGIC
# MAGIC - **Lineage** shows the full chain: which notebooks, tables, and files feed into a given table. If the Gold table looks wrong, lineage helps you trace back to the source.
# MAGIC - **Permissions** control who can SELECT, MODIFY, or manage each table. In production, you'd grant analysts SELECT on Gold tables but restrict access to Bronze.
# MAGIC - **Insights** show query activity: who's querying the table, how often, and what kinds of queries they run. Useful for understanding which tables are actually being used.
# MAGIC
# MAGIC </details>
# MAGIC
# MAGIC </div>

# COMMAND ----------

# MAGIC %md-sandbox
# MAGIC
# MAGIC <!-- Micro-win summary -->
# MAGIC
# MAGIC <div style="max-width: 900px; margin: 0 auto; font-family: sans-serif;">
# MAGIC <div style="margin-top: 10px; padding: 18px 24px; background: #FFF6F4; border: 3px solid #FF5F46; border-radius: 10px;">
# MAGIC   <div style="font-size: 14pt; color: #0b2026; line-height: 1.6;">
# MAGIC     <div style="font-weight: 700; margin-bottom: 8px;">What you just did:</div>
# MAGIC     <ul style="padding-left: 20px; margin: 0;">
# MAGIC       <li>Created a <strong>Bronze</strong> table with raw data using <code>COPY INTO</code></li>
# MAGIC       <li>Created a <strong>Silver</strong> table with transformations (<code>UPPER</code>, audit timestamps)</li>
# MAGIC       <li>Created a <strong>Gold</strong> table with aggregated, business-ready data</li>
# MAGIC       <li>Used the <code>INSERT OVERWRITE</code> pattern for refreshable Gold tables</li>
# MAGIC       <li>Explored <strong>lineage</strong>, <strong>permissions</strong>, and <strong>insights</strong> in Catalog Explorer</li>
# MAGIC     </ul>
# MAGIC     <div style="margin-top: 12px;">You've built a complete Medallion Architecture pipeline by hand. </div>
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
# MAGIC     <p>In this lesson, you built a complete Medallion Architecture pipeline:</p>
# MAGIC     <ul style="padding-left: 20px; margin: 8px 0;">
# MAGIC       <li><strong>Bronze</strong> — raw data ingested from CSV files with <code>COPY INTO</code></li>
# MAGIC       <li><strong>Silver</strong> — cleaned and enriched with transformations and audit timestamps</li>
# MAGIC       <li><strong>Gold</strong> — aggregated for business consumption with <code>INSERT OVERWRITE</code></li>
# MAGIC     </ul>
# MAGIC     <p>You also explored how Unity Catalog automatically tracks lineage, permissions, and usage across all three layers.</p>
# MAGIC   </div>
# MAGIC </div>
# MAGIC
# MAGIC <div style="margin-top: 16px; padding: 16px 20px; background: #F8F9FC; border-left: 4px solid #1B5162; border-radius: 6px;">
# MAGIC   <div style="font-size: 14pt; color: #0b2026; line-height: 1.6;">
# MAGIC     <strong>Quick self-check:</strong> Could you explain to a teammate why data goes through three layers instead of loading it straight into a final table?
# MAGIC   </div>
# MAGIC </div>
# MAGIC
# MAGIC
