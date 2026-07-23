# Databricks notebook source
# MAGIC %md-sandbox
# MAGIC
# MAGIC <div style="max-width: 1000px; margin: 0 auto; font-family: sans-serif;">
# MAGIC
# MAGIC <div style="background: #1B5162; color: white; border-radius: 8px; padding: 28px 32px; text-align: center; position: relative;">
# MAGIC   <div style="font-size: 14pt; font-weight: 600; text-transform: uppercase; letter-spacing: 1px; opacity: 0.85; margin-bottom: 8px;">Lesson 5</div>
# MAGIC   <div style="font-size: 24pt; font-weight: 700; line-height: 1.3;">Load Data Incrementally with COPY INTO</div>
# MAGIC   <div style="font-size: 14pt; margin-top: 12px; opacity: 0.9;">Use COPY INTO to load data into an existing table, verify its idempotency, and understand incremental ingestion.</div>
# MAGIC </div>
# MAGIC
# MAGIC </div>

# COMMAND ----------


# MAGIC %md
# MAGIC **Where we left off:** You created tables with CTAS (code-driven, one-time) and the Upload UI (manual, one-time). Now you'll learn the method used for repeatable, incremental pipelines.

# COMMAND ----------

# MAGIC %md-sandbox
# MAGIC
# MAGIC <!-- LEARN: COPY INTO -->
# MAGIC <!-- Template: numbered-steps-with-examples-summary (adapted) -->
# MAGIC
# MAGIC <div style="max-width: 900px; margin: 0 auto; font-family: sans-serif;">
# MAGIC
# MAGIC <div style="font-size: 20pt; font-weight: 700; color: #0b2026; margin-bottom: 6px;">COPY INTO: Safe, Incremental File Loading</div>
# MAGIC <div style="font-size: 14pt; color: #5A6F77; margin-bottom: 24px;">Unlike CTAS (which creates a new table each time), COPY INTO loads files into an existing table and tracks which files have already been processed. This makes it safe to re-run on a schedule.</div>
# MAGIC
# MAGIC <div style="display: flex; flex-direction: column; gap: 16px;">
# MAGIC
# MAGIC <!-- Step 1 -->
# MAGIC <div style="background: #F9F7F4; border-radius: 8px; box-shadow: 0 2px 8px rgba(27,49,57,0.06); padding: 18px 20px; position: relative;">
# MAGIC   <div style="position: absolute; top: 0; left: 0; width: 100%; height: 6px; background: #2574B5; border-radius: 8px 8px 0 0;"></div>
# MAGIC   <div style="display: flex; align-items: center; gap: 12px; margin-bottom: 8px;">
# MAGIC     <div style="font-size: 18pt; font-weight: 800; color: #0b2026;">1</div>
# MAGIC     <div style="font-size: 18pt; font-weight: 700; color: #0b2026;">Create an empty table with a defined schema</div>
# MAGIC   </div>
# MAGIC   <div style="font-size: 14pt; color: #0b2026; line-height: 1.6;">
# MAGIC     COPY INTO loads into an existing table, so you create the table first with the columns and data types you expect.
# MAGIC   </div>
# MAGIC </div>
# MAGIC
# MAGIC <!-- Step 2 -->
# MAGIC <div style="background: #F9F7F4; border-radius: 8px; box-shadow: 0 2px 8px rgba(27,49,57,0.06); padding: 18px 20px; position: relative;">
# MAGIC   <div style="position: absolute; top: 0; left: 0; width: 100%; height: 6px; background: #02A36F; border-radius: 8px 8px 0 0;"></div>
# MAGIC   <div style="display: flex; align-items: center; gap: 12px; margin-bottom: 8px;">
# MAGIC     <div style="font-size: 18pt; font-weight: 800; color: #0b2026;">2</div>
# MAGIC     <div style="font-size: 18pt; font-weight: 700; color: #0b2026;">Run COPY INTO to load all files from a directory</div>
# MAGIC   </div>
# MAGIC   <div style="font-size: 14pt; color: #0b2026; line-height: 1.6;">
# MAGIC     Point COPY INTO at a volume path. It reads every file in that directory and loads the data into your table. It records which files it processed.
# MAGIC   </div>
# MAGIC </div>
# MAGIC
# MAGIC <!-- Step 3 -->
# MAGIC <div style="background: #F9F7F4; border-radius: 8px; box-shadow: 0 2px 8px rgba(27,49,57,0.06); padding: 18px 20px; position: relative;">
# MAGIC   <div style="position: absolute; top: 0; left: 0; width: 100%; height: 6px; background: #F8A805; border-radius: 8px 8px 0 0;"></div>
# MAGIC   <div style="display: flex; align-items: center; gap: 12px; margin-bottom: 8px;">
# MAGIC     <div style="font-size: 18pt; font-weight: 800; color: #0b2026;">3</div>
# MAGIC     <div style="font-size: 18pt; font-weight: 700; color: #0b2026;">Re-run safely — only new files get loaded</div>
# MAGIC   </div>
# MAGIC   <div style="font-size: 14pt; color: #0b2026; line-height: 1.6;">
# MAGIC     If you run COPY INTO again on the same directory, it loads <strong>0 rows</strong> because it already processed those files. If a new file lands in the directory, only that file gets loaded. This is called <strong>idempotency</strong>.
# MAGIC   </div>
# MAGIC </div>
# MAGIC
# MAGIC </div>
# MAGIC
# MAGIC <!-- Key takeaway -->
# MAGIC <div style="margin-top: 16px; padding: 16px 20px; background: #FFF6F4; border: 3px solid #FF5F46; border-radius: 10px;">
# MAGIC   <div style="font-size: 14pt; color: #0b2026; line-height: 1.6;">
# MAGIC     <strong>Key takeaway:</strong> COPY INTO is safe to run on a schedule because it never double-loads data. For production workloads at scale, Databricks recommends streaming tables as a more scalable alternative, but the incremental loading concept is the same.
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
# MAGIC **How COPY INTO compares to CTAS**
# MAGIC
# MAGIC - **CTAS** creates a new table every time. If you run it twice, you get an error (table already exists) or overwrite the table. It's a one-time operation.
# MAGIC - **COPY INTO** loads into an existing table. It tracks which files have been processed using the table's transaction log, so re-running it is safe and only picks up new files.
# MAGIC - Think of CTAS as "create the table from scratch" and COPY INTO as "add new data to the table."
# MAGIC
# MAGIC **When to use COPY INTO**
# MAGIC
# MAGIC - You have a volume where new files land regularly (daily exports, partner data drops, sensor readings)
# MAGIC - You want to run a scheduled job that picks up new files without reprocessing old ones
# MAGIC - You need a simple, SQL-based incremental loading pattern
# MAGIC
# MAGIC **Limitations to know**
# MAGIC
# MAGIC - COPY INTO tracks files by path. If you overwrite a file with the same name but different content, COPY INTO won't re-process it.
# MAGIC - For high-volume, low-latency streaming, Databricks recommends streaming tables (Auto Loader under the hood) instead of COPY INTO.
# MAGIC
# MAGIC </details>
# MAGIC
# MAGIC </div>

# COMMAND ----------

# MAGIC %md
# MAGIC ### Explore: Create an empty table with a defined schema
# MAGIC
# MAGIC Unlike CTAS, COPY INTO loads data into an existing table. So first, we create an empty table with the columns and types we expect.

# COMMAND ----------

# MAGIC %sql
# MAGIC USE CATALOG dbacademy;
# MAGIC USE SCHEMA get_started_de;
# MAGIC
# MAGIC CREATE TABLE IF NOT EXISTS current_employees_copyinto (
# MAGIC   ID INT,
# MAGIC   FirstName STRING,
# MAGIC   Country STRING,
# MAGIC   Role STRING
# MAGIC );

# COMMAND ----------

# MAGIC %sql
# MAGIC SELECT * FROM current_employees_copyinto;

# COMMAND ----------

# MAGIC %md
# MAGIC The table exists but has **0 rows**. Now let's load data into it.

# COMMAND ----------

# MAGIC %md
# MAGIC ### Explore: Load data with COPY INTO
# MAGIC
# MAGIC COPY INTO reads all CSV files from the volume directory and loads them into the table. Both `employees.csv` (4 rows) and `employees2.csv` (2 rows) are in the directory, so we should get 6 rows total.

# COMMAND ----------

result = spark.sql(f"""
    COPY INTO current_employees_copyinto
    FROM '/Volumes/dbacademy/get_started_de/myfiles/'
    FILEFORMAT = CSV
    FORMAT_OPTIONS ('header' = 'true', 'inferSchema' = 'true')
""")
result.display()

# COMMAND ----------

# MAGIC %md
# MAGIC The **num_affected_rows** column should show **6** — 4 rows from `employees.csv` and 2 from `employees2.csv`. COPY INTO loaded both files in one pass.

# COMMAND ----------

# MAGIC %sql
# MAGIC SELECT * FROM current_employees_copyinto;

# COMMAND ----------

# MAGIC %md
# MAGIC All 6 employees are in the table.

# COMMAND ----------

# MAGIC %md
# MAGIC ### Explore: Prove idempotency: re-run the same COPY INTO
# MAGIC
# MAGIC What happens if you run the exact same COPY INTO command again? Let's find out.

# COMMAND ----------

result = spark.sql(f"""
    COPY INTO current_employees_copyinto
    FROM '/Volumes/dbacademy/get_started_de/myfiles/'
    FILEFORMAT = CSV
    FORMAT_OPTIONS ('header' = 'true', 'inferSchema' = 'true')
""")
result.display()

# COMMAND ----------

# MAGIC %md
# MAGIC **num_affected_rows: 0**. COPY INTO remembered that it already processed both files and skipped them. No duplicate data. This is what makes it safe to run on a schedule — if no new files have arrived, nothing happens.

# COMMAND ----------

# MAGIC %md
# MAGIC ### Explore: Verify the version history
# MAGIC
# MAGIC Let's confirm what COPY INTO recorded in the table's transaction log.

# COMMAND ----------

# MAGIC %sql
# MAGIC DESCRIBE HISTORY current_employees_copyinto;

# COMMAND ----------

# MAGIC %md
# MAGIC You should see:
# MAGIC - **Version 0** — `CREATE TABLE` (the empty table)
# MAGIC - **Version 1** — `COPY INTO` (loaded 6 rows from 2 files)
# MAGIC
# MAGIC Notice there's no version 2 for the second COPY INTO run — since it loaded 0 rows, no new version was created. The table is unchanged.

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
# MAGIC       <li>Created an empty table with a defined schema</li>
# MAGIC       <li>Loaded 6 rows from 2 CSV files using <code>COPY INTO</code></li>
# MAGIC       <li>Proved idempotency — re-running loaded 0 rows because the files were already processed</li>
# MAGIC       <li>Verified the transaction log only records actual changes</li>
# MAGIC     </ul>
# MAGIC     <div style="margin-top: 12px;">You now know three ingestion methods: <strong>CTAS</strong> (one-time, code-driven), <strong>Upload UI</strong> (one-time, manual), and <strong>COPY INTO</strong> (incremental, schedule-safe).</div>
# MAGIC   </div>
# MAGIC </div>
# MAGIC </div>
