# Databricks notebook source
# MAGIC %md-sandbox
# MAGIC
# MAGIC <div style="max-width: 1000px; margin: 0 auto; font-family: sans-serif;">
# MAGIC
# MAGIC <div style="background: #02A36F; color: white; border-radius: 8px; padding: 28px 32px; text-align: center; position: relative;">
# MAGIC   <div style="font-size: 14pt; font-weight: 600; text-transform: uppercase; letter-spacing: 1px; opacity: 0.85; margin-bottom: 8px;">Practice</div>
# MAGIC   <div style="font-size: 24pt; font-weight: 700; line-height: 1.3;">Load Data Incrementally</div>
# MAGIC   <div style="font-size: 14pt; margin-top: 12px; opacity: 0.9;">Practice creating an empty table and loading data into it with COPY INTO.</div>
# MAGIC </div>
# MAGIC
# MAGIC </div>

# COMMAND ----------


# MAGIC %md
# MAGIC ### Instructions
# MAGIC
# MAGIC In Lesson 5, you used COPY INTO to load both CSV files into `current_employees_copyinto`. Now you'll practice the same pattern from scratch: create an empty table, load data, and prove it's idempotent.
# MAGIC
# MAGIC Your goal: create a table called **`practice_copyinto`**, load the CSV files into it, and verify the behavior.

# COMMAND ----------

# MAGIC %md
# MAGIC ### Task 1: Create an empty table
# MAGIC
# MAGIC Create a table called `practice_copyinto` with 4 columns: `ID` (INT), `FirstName` (STRING), `Country` (STRING), `Role` (STRING).

# COMMAND ----------

# MAGIC %sql
# MAGIC USE CATALOG dbacademy;
# MAGIC USE SCHEMA get_started_de;
# MAGIC
# MAGIC -- TODO: Create an empty table called practice_copyinto with the correct schema
# MAGIC <FILL_IN>

# COMMAND ----------

# MAGIC %md-sandbox
# MAGIC <details>
# MAGIC <summary>Hint</summary>
# MAGIC
# MAGIC <pre><code>CREATE TABLE IF NOT EXISTS practice_copyinto (
# MAGIC   ID INT,
# MAGIC   FirstName STRING,
# MAGIC   Country STRING,
# MAGIC   Role STRING
# MAGIC );</code></pre>
# MAGIC
# MAGIC </details>

# COMMAND ----------

# MAGIC %md
# MAGIC Verify the table is empty.

# COMMAND ----------

# MAGIC %sql
# MAGIC SELECT COUNT(*) AS row_count FROM practice_copyinto;

# COMMAND ----------

# MAGIC %md
# MAGIC ### Task 2: Load data with COPY INTO
# MAGIC
# MAGIC Use COPY INTO to load all CSV files from the `myfiles` volume into `practice_copyinto`. Use the Python cell below (COPY INTO requires `spark.sql` in notebooks).

# COMMAND ----------

# TODO: Run COPY INTO to load CSV files from the volume into practice_copyinto
# Replace the <FILL_IN> placeholders
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
# MAGIC     COPY INTO practice_copyinto
# MAGIC     FROM '/Volumes/dbacademy/get_started_de/myfiles/'
# MAGIC     FILEFORMAT = CSV
# MAGIC     FORMAT_OPTIONS ('header' = 'true', 'inferSchema' = 'true')
# MAGIC """)
# MAGIC result.display()</code></pre>
# MAGIC
# MAGIC </details>

# COMMAND ----------

# MAGIC %md
# MAGIC You should see **num_affected_rows: 6** (4 from `employees.csv` + 2 from `employees2.csv`).

# COMMAND ----------

# MAGIC %md
# MAGIC ### Task 3: Verify the data
# MAGIC
# MAGIC Query the table to confirm all 6 rows loaded.

# COMMAND ----------

# MAGIC %sql
# MAGIC -- TODO: Query practice_copyinto
# MAGIC <FILL_IN>

# COMMAND ----------

# MAGIC %md-sandbox
# MAGIC <details>
# MAGIC <summary>Hint</summary>
# MAGIC
# MAGIC <pre><code>SELECT * FROM practice_copyinto;</code></pre>
# MAGIC
# MAGIC </details>

# COMMAND ----------

# MAGIC %md
# MAGIC ### Task 4: Prove idempotency
# MAGIC
# MAGIC Run the exact same COPY INTO command again. How many rows get loaded this time?

# COMMAND ----------

# TODO: Re-run the same COPY INTO command
result = spark.sql("""
    COPY INTO practice_copyinto
    FROM '/Volumes/dbacademy/get_started_de/myfiles/'
    FILEFORMAT = CSV
    FORMAT_OPTIONS ('header' = 'true', 'inferSchema' = 'true')
""")
result.display()

# COMMAND ----------

# MAGIC %md
# MAGIC **num_affected_rows: 0**. The files were already processed. No duplicates.

# COMMAND ----------

# MAGIC %md
# MAGIC ### Task 5: Check the version history
# MAGIC
# MAGIC Use `DESCRIBE HISTORY` to confirm that only the initial load created a new version, not the re-run.

# COMMAND ----------

# MAGIC %sql
# MAGIC -- TODO: Show version history of practice_copyinto
# MAGIC <FILL_IN>

# COMMAND ----------

# MAGIC %md-sandbox
# MAGIC <details>
# MAGIC <summary>Hint</summary>
# MAGIC
# MAGIC <pre><code>DESCRIBE HISTORY practice_copyinto;</code></pre>
# MAGIC
# MAGIC </details>

# COMMAND ----------

# MAGIC %md-sandbox
# MAGIC
# MAGIC <div style="max-width: 900px; margin: 0 auto; font-family: sans-serif;">
# MAGIC <div style="margin-top: 10px; padding: 18px 24px; background: #FFF6F4; border: 3px solid #FF5F46; border-radius: 10px;">
# MAGIC   <div style="font-size: 14pt; color: #0b2026; line-height: 1.6;">
# MAGIC     <div style="font-weight: 700; margin-bottom: 8px;">Nice work! You just:</div>
# MAGIC     <ul style="padding-left: 20px; margin: 0;">
# MAGIC       <li>Created an empty table with a defined schema</li>
# MAGIC       <li>Loaded data incrementally with <code>COPY INTO</code></li>
# MAGIC       <li>Proved idempotency by re-running and getting 0 rows</li>
# MAGIC       <li>Verified the transaction log only records actual data changes</li>
# MAGIC     </ul>
# MAGIC   </div>
# MAGIC </div>
# MAGIC </div>

# COMMAND ----------

# MAGIC %md-sandbox
# MAGIC
# MAGIC <!-- CHECKPOINT: Lessons 4-5 -->
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
# MAGIC     <p>Over Lessons 4 and 5, you learned three ingestion methods:</p>
# MAGIC     <ul style="padding-left: 20px; margin: 8px 0;">
# MAGIC       <li><strong>CTAS</strong> — code-driven, one-time table creation with full control over columns and format options</li>
# MAGIC       <li><strong>Upload UI</strong> — manual drag-and-drop for quick, ad-hoc imports</li>
# MAGIC       <li><strong>COPY INTO</strong> — incremental loading that's safe to re-run because it tracks which files have already been processed</li>
# MAGIC     </ul>
# MAGIC     <p>Combined with Lessons 1 through 3, you can now find raw data, create tables, modify their contents, audit every change, and choose the right ingestion method for the job.</p>
# MAGIC   </div>
# MAGIC </div>
# MAGIC
# MAGIC <div style="margin-top: 16px; padding: 16px 20px; background: #F8F9FC; border-left: 4px solid #1B5162; border-radius: 6px;">
# MAGIC   <div style="font-size: 14pt; color: #0b2026; line-height: 1.6;">
# MAGIC     <strong>Quick self-check:</strong> If a teammate asked "what's the difference between CTAS and COPY INTO?" could you explain when you'd use each one?
# MAGIC   </div>
# MAGIC </div>
