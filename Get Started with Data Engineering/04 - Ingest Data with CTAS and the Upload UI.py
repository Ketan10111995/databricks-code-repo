# Databricks notebook source
# MAGIC %md-sandbox
# MAGIC
# MAGIC <div style="max-width: 1000px; margin: 0 auto; font-family: sans-serif;">
# MAGIC
# MAGIC <div style="background: #1B5162; color: white; border-radius: 8px; padding: 28px 32px; text-align: center; position: relative;">
# MAGIC   <div style="font-size: 14pt; font-weight: 600; text-transform: uppercase; letter-spacing: 1px; opacity: 0.85; margin-bottom: 8px;">Lesson 4</div>
# MAGIC   <div style="font-size: 24pt; font-weight: 700; line-height: 1.3;">Ingest Data with CTAS and the Upload UI</div>
# MAGIC   <div style="font-size: 14pt; margin-top: 12px; opacity: 0.9;">Create Delta tables from files using two methods: CREATE TABLE AS SELECT with format options and the Catalog Explorer upload interface.</div>
# MAGIC </div>
# MAGIC
# MAGIC </div>

# COMMAND ----------


# MAGIC %md
# MAGIC **In this lesson:** You'll learn different ways to get data *into* tables.

# COMMAND ----------

# MAGIC %md-sandbox
# MAGIC
# MAGIC <!-- LEARN: Two ingestion methods -->
# MAGIC <!-- Template: 2-card-colored-header-guidance -->
# MAGIC
# MAGIC <div style="max-width: 950px; margin: 0 auto; font-family: sans-serif; color: #0b2026;">
# MAGIC
# MAGIC <div style="font-size: 20pt; font-weight: 700; color: #0b2026; margin-bottom: 6px;">Two Ways to Create a Table from a File</div>
# MAGIC <div style="font-size: 14pt; color: #5A6F77; margin-bottom: 24px;">Both methods produce a Delta table, but they serve different purposes.</div>
# MAGIC
# MAGIC <div style="display: flex; gap: 20px; justify-content: center;">
# MAGIC
# MAGIC <!-- Card 1: CTAS -->
# MAGIC <div style="flex: 1; border: 2px solid #e0e0e0; border-radius: 12px; overflow: hidden; background: white;">
# MAGIC   <div style="background: #4299E0; color: white; padding: 14px 20px; text-align: center;">
# MAGIC     <div style="font-size: 18pt; font-weight: bold;">CREATE TABLE AS SELECT</div>
# MAGIC   </div>
# MAGIC   <div style="padding: 18px 20px;">
# MAGIC     <div style="font-size: 14pt; color: #555; line-height: 1.6; margin-bottom: 14px;">
# MAGIC       Write SQL to read a file and define exactly which columns to include, what format options to apply, and how the table should be structured. Repeatable and version-controlled.
# MAGIC     </div>
# MAGIC     <div style="background: rgba(66,153,224,0.10); border-left: 4px solid #4299E0; padding: 10px 12px; border-radius: 6px; font-size: 14pt;">
# MAGIC       <strong>Use when:</strong> You're building a pipeline, need reproducibility, or want to select specific columns from the source file.
# MAGIC     </div>
# MAGIC   </div>
# MAGIC </div>
# MAGIC
# MAGIC <!-- Card 2: Upload UI -->
# MAGIC <div style="flex: 1; border: 2px solid #e0e0e0; border-radius: 12px; overflow: hidden; background: white;">
# MAGIC   <div style="background: #00A972; color: white; padding: 14px 20px; text-align: center;">
# MAGIC     <div style="font-size: 18pt; font-weight: bold;">Catalog Explorer Upload</div>
# MAGIC   </div>
# MAGIC   <div style="padding: 18px 20px;">
# MAGIC     <div style="font-size: 14pt; color: #555; line-height: 1.6; margin-bottom: 14px;">
# MAGIC       Drag and drop a file in the Catalog Explorer UI. Databricks auto-detects the format, infers the schema, and creates the table. No code required.
# MAGIC     </div>
# MAGIC     <div style="background: rgba(0,169,114,0.10); border-left: 4px solid #00A972; padding: 10px 12px; border-radius: 6px; font-size: 14pt;">
# MAGIC       <strong>Use when:</strong> Someone hands you a CSV and you need it in a table fast. Quick, ad-hoc imports where reproducibility is not a concern.
# MAGIC     </div>
# MAGIC   </div>
# MAGIC </div>
# MAGIC
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
# MAGIC **Choosing between the two methods**
# MAGIC
# MAGIC - **CTAS** is the workhorse of data engineering. You write SQL that reads from a source (file, another table, or an external system), optionally transforms the data, and writes the result as a new table. Because it's code, it's repeatable: you can re-run it, put it in a pipeline, and version-control it in Git.
# MAGIC - **Upload UI** is for convenience. When an analyst emails you a spreadsheet and you need to query it quickly, dragging it into Catalog Explorer is faster than writing a CTAS statement. But it's manual and not repeatable.
# MAGIC - In Lesson 1, you used a basic CTAS without any format options: `CREATE TABLE AS SELECT * FROM read_files(...)`. In this lesson, you'll use explicit format options to control how the file is read.
# MAGIC - The format options (`format`, `header`, `inferSchema`) tell `read_files` exactly how to parse the file. This matters when files don't have headers, use a non-standard delimiter, or have ambiguous data types.
# MAGIC
# MAGIC </details>
# MAGIC
# MAGIC </div>

# COMMAND ----------

# MAGIC %md
# MAGIC ### Explore: Create a table with CTAS and format options
# MAGIC
# MAGIC In Lesson 1, you used a basic CTAS: `CREATE TABLE AS SELECT * FROM read_files(...)`. Now let's use explicit format options to control exactly how the file is read.

# COMMAND ----------

# MAGIC %sql
# MAGIC USE CATALOG dbacademy;
# MAGIC USE SCHEMA get_started_de;
# MAGIC
# MAGIC CREATE TABLE IF NOT EXISTS current_employees_ctas AS
# MAGIC SELECT ID, FirstName, Country, Role
# MAGIC FROM read_files(
# MAGIC   '/Volumes/dbacademy/get_started_de/myfiles/employees.csv',
# MAGIC   format => 'csv',
# MAGIC   header => true,
# MAGIC   inferSchema => true
# MAGIC );

# COMMAND ----------

# MAGIC %md
# MAGIC Notice the differences from Lesson 1:
# MAGIC - **`format => 'csv'`** — explicitly tells Databricks this is a CSV file (instead of auto-detecting)
# MAGIC - **`header => true`** — the first row contains column names, not data
# MAGIC - **`inferSchema => true`** — automatically detect data types for each column
# MAGIC - **`SELECT ID, FirstName, Country, Role`** — we selected only the 4 data columns, excluding the `_rescued_data` column that `read_files` adds automatically

# COMMAND ----------

# MAGIC %sql
# MAGIC SELECT * FROM current_employees_ctas;

# COMMAND ----------

# MAGIC %md
# MAGIC You should see 4 rows with exactly 4 columns. By selecting specific columns in the CTAS, you get a clean table without the extra `_rescued_data` column.

# COMMAND ----------

# MAGIC %md
# MAGIC ### Explore: Create a table using the Catalog Explorer Upload UI
# MAGIC
# MAGIC The second method uses no code at all. You upload a file through the Catalog Explorer interface and Databricks creates the table for you.
# MAGIC
# MAGIC **Follow these steps:**
# MAGIC
# MAGIC 1. In the left sidebar, click **Catalog** to open Catalog Explorer
# MAGIC 2. Navigate to your catalog (`dbacademy`) → your schema (`get_started_de`)
# MAGIC 3. Click the **Create** button and select **Table**
# MAGIC 4. Drag and drop the `employees.csv` file, or click **browse** to select it
# MAGIC    - If you need to download the file first: go to **Volumes** → **myfiles** → click `employees.csv` → click **Download**
# MAGIC 5. Databricks auto-detects the format and infers the schema — review the preview
# MAGIC 6. Set the table name to **`current_employees_ui`**
# MAGIC 7. Click **Create table**
# MAGIC
# MAGIC Once you've created the table, verify it exists by running the cell below.

# COMMAND ----------

# Run this after completing the Upload UI steps above.
try:
    display(spark.sql("SELECT * FROM current_employees_ui"))
except Exception as e:
    if "TABLE_OR_VIEW_NOT_FOUND" in str(e):
        print("The table 'current_employees_ui' doesn't exist yet.")
        print("Complete the Upload UI steps above, then re-run this cell.")
    else:
        raise e

# COMMAND ----------

# MAGIC %md
# MAGIC ### Explore: Compare both tables
# MAGIC
# MAGIC Let's verify that both methods produced the same data.

# COMMAND ----------

# MAGIC %sql
# MAGIC SHOW TABLES;

# COMMAND ----------

# MAGIC %md
# MAGIC You should see both `current_employees_ctas` and `current_employees_ui` listed, along with `employees` from Lesson 1 (and any other tables you created in the practice exercises). Two tables, two methods, same source data.

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
# MAGIC       <li>Created a table with <code>CTAS</code> using explicit format options (<code>format</code>, <code>header</code>, <code>inferSchema</code>)</li>
# MAGIC       <li>Selected specific columns to produce a clean table without <code>_rescued_data</code></li>
# MAGIC       <li>Created a table using the Catalog Explorer Upload UI with no code</li>
# MAGIC       <li>Verified both methods produced working Delta tables</li>
# MAGIC     </ul>
# MAGIC     <div style="margin-top: 12px;"><strong>CTAS</strong> is code-driven and repeatable. The <strong>Upload UI</strong> is fast but manual.</div>
# MAGIC   </div>
# MAGIC </div>
# MAGIC </div>
