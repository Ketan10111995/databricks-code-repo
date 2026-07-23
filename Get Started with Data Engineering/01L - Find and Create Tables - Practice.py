# Databricks notebook source
# MAGIC %md-sandbox
# MAGIC
# MAGIC <div style="max-width: 1000px; margin: 0 auto; font-family: sans-serif;">
# MAGIC
# MAGIC <div style="background: #02A36F; color: white; border-radius: 8px; padding: 28px 32px; text-align: center; position: relative;">
# MAGIC   <div style="font-size: 14pt; font-weight: 600; text-transform: uppercase; letter-spacing: 1px; opacity: 0.85; margin-bottom: 8px;">Practice</div>
# MAGIC   <div style="font-size: 24pt; font-weight: 700; line-height: 1.3;">Find and Create Tables</div>
# MAGIC   <div style="font-size: 14pt; margin-top: 12px; opacity: 0.9;">Apply what you learned in Lesson 1 to preview a new data file and create a Delta table from it on your own.</div>
# MAGIC </div>
# MAGIC
# MAGIC </div>

# COMMAND ----------

# MAGIC
# MAGIC %md
# MAGIC ### Instructions
# MAGIC
# MAGIC In Lesson 1, you found `employees.csv` in your volume and created a Delta table from it. But there was a second file in that volume: **`employees2.csv`**.
# MAGIC
# MAGIC In this practice, you will:
# MAGIC 1. List the files in the volume to confirm `employees2.csv` is there
# MAGIC 2. Preview the contents of `employees2.csv`
# MAGIC 3. Create a new Delta table called `new_employees` from that file
# MAGIC 4. Query your new table to verify it worked
# MAGIC
# MAGIC Replace the `<FILL_IN>` placeholders below with the correct SQL. If you get stuck, expand the hint under each task.

# COMMAND ----------

# MAGIC %md
# MAGIC ### Task 1: List the files in the volume
# MAGIC
# MAGIC Confirm that `employees2.csv` exists alongside `employees.csv`.

# COMMAND ----------

# MAGIC %sql
# MAGIC USE CATALOG ketancatalog;
# MAGIC USE SCHEMA ketanschema;

# COMMAND ----------

# MAGIC %md-sandbox
# MAGIC <details>
# MAGIC <summary>Hint</summary>
# MAGIC
# MAGIC The volume path is `/Volumes/dbacademy/get_started_de/myfiles/`
# MAGIC
# MAGIC </details>

# COMMAND ----------

# MAGIC %md
# MAGIC ### Task 2: Preview the new CSV file
# MAGIC
# MAGIC Use `read_files` to peek at the contents of `employees2.csv` before creating a table.

# COMMAND ----------


df=spark.read.csv('/Volumes/ketancatalog/ketanschema/myfiles/employees2.csv',header=True,inferSchema=True)
df.display()

# COMMAND ----------

# MAGIC %md-sandbox
# MAGIC <details>
# MAGIC <summary>Hint</summary>
# MAGIC
# MAGIC The full path to the file is `/Volumes/dbacademy/get_started_de/myfiles/employees2.csv`
# MAGIC
# MAGIC </details>

# COMMAND ----------

# MAGIC %md
# MAGIC You should see **2 rows** with the same columns as the original file: ID, FirstName, Country, and Role. These are new employees that haven't been added to a table yet.

# COMMAND ----------

# MAGIC %md
# MAGIC ### Task 3: Create a Delta table from the new file
# MAGIC
# MAGIC Use `CREATE TABLE AS SELECT` to create a table called **`new_employees`** from `employees2.csv`.

# COMMAND ----------

df.write.saveAsTable('ketancatalog.ketanschema.employees2', mode='overwrite')

# COMMAND ----------

# MAGIC %md-sandbox
# MAGIC <details>
# MAGIC <summary>Hint</summary>
# MAGIC
# MAGIC The pattern is the same as Lesson 1:
# MAGIC <pre><code>CREATE TABLE IF NOT EXISTS new_employees
# MAGIC AS SELECT * FROM read_files('/Volumes/dbacademy/get_started_de/myfiles/employees2.csv');</code></pre>
# MAGIC
# MAGIC </details>

# COMMAND ----------

# MAGIC %md
# MAGIC ### Task 4: Verify your new table
# MAGIC
# MAGIC Query the `new_employees` table to confirm it has the expected data.

# COMMAND ----------

# MAGIC %sql
# MAGIC select * from ketancatalog.ketanschema.employees2;

# COMMAND ----------

# MAGIC %md-sandbox
# MAGIC <details>
# MAGIC <summary>Hint</summary>
# MAGIC
# MAGIC <pre><code>SELECT * FROM new_employees;</code></pre>
# MAGIC
# MAGIC </details>

# COMMAND ----------

# MAGIC %md
# MAGIC ### Task 5: Check your schema
# MAGIC
# MAGIC Run `SHOW TABLES` to see all the tables in your schema. You should now see both `employees` (from Lesson 1) and `new_employees` (from this practice).

# COMMAND ----------

# MAGIC %sql
# MAGIC SHOW TABLES;

# COMMAND ----------

# MAGIC %md-sandbox
# MAGIC
# MAGIC <div style="max-width: 900px; margin: 0 auto; font-family: sans-serif;">
# MAGIC <div style="margin-top: 10px; padding: 18px 24px; background: #FFF6F4; border: 3px solid #FF5F46; border-radius: 10px;">
# MAGIC   <div style="font-size: 14pt; color: #0b2026; line-height: 1.6;">
# MAGIC     <div style="font-weight: 700; margin-bottom: 8px;">Nice work! You just:</div>
# MAGIC     <ul style="padding-left: 20px; margin: 0;">
# MAGIC       <li>Found a second data file in your volume</li>
# MAGIC       <li>Previewed it with <code>read_files</code> before committing to a table</li>
# MAGIC       <li>Created a new Delta table using <code>CREATE TABLE AS SELECT</code></li>
# MAGIC       <li>Verified the table exists alongside your Lesson 1 table</li>
# MAGIC     </ul>
# MAGIC     <div style="margin-top: 12px;">You now have two tables in your schema, and both were created from raw CSV files using the same pattern.</div>
# MAGIC   </div>
# MAGIC </div>
# MAGIC </div>
