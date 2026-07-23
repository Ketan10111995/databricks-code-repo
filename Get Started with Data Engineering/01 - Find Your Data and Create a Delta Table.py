# Databricks notebook source
# MAGIC %md-sandbox
# MAGIC
# MAGIC <div style="max-width: 1000px; margin: 0 auto; font-family: sans-serif;">
# MAGIC
# MAGIC <div style="background: #1B5162; color: white; border-radius: 8px; padding: 28px 32px; text-align: center; position: relative;">
# MAGIC   <div style="font-size: 14pt; font-weight: 600; text-transform: uppercase; letter-spacing: 1px; opacity: 0.85; margin-bottom: 8px;">Lesson 1</div>
# MAGIC   <div style="font-size: 24pt; font-weight: 700; line-height: 1.3;">Find Your Data and Create a Delta Table</div>
# MAGIC   <div style="font-size: 14pt; margin-top: 12px; opacity: 0.9;">Navigate the catalog hierarchy, locate a raw data file, preview its contents, and create a Delta table from it.</div>
# MAGIC </div>
# MAGIC
# MAGIC </div>

# COMMAND ----------

# MAGIC
# MAGIC %md-sandbox
# MAGIC
# MAGIC <!-- LEARN: Unity Catalog Hierarchy -->
# MAGIC <!-- Template: vertical-layered-stack (adapted to 3 layers) -->
# MAGIC
# MAGIC <div style="max-width: 900px; margin: 0 auto; font-family: sans-serif;">
# MAGIC
# MAGIC <div style="font-size: 20pt; font-weight: 700; color: #0b2026; margin-bottom: 6px;">How Databricks Organizes Your Data</div>
# MAGIC <div style="font-size: 14pt; color: #5A6F77; margin-bottom: 24px;">Everything in Databricks lives in a three-level hierarchy within Unity Catalog. Think of it like folders on your computer, except these folders also control who can see and use the data inside them.</div>
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
# MAGIC &larr; BROAD TO SPECIFIC
# MAGIC </div>
# MAGIC
# MAGIC <!-- Stacked layers -->
# MAGIC <div style="flex: 1; display: flex; flex-direction: column; gap: 6px;">
# MAGIC
# MAGIC <!-- Catalog -->
# MAGIC <div style="background: #1C3037; color: white; border-radius: 8px 8px 4px 4px; padding: 22px 24px; text-align: center;">
# MAGIC   <div style="font-size: 18pt; font-weight: 700;">Catalog</div>
# MAGIC   <div style="font-size: 14pt; margin-top: 6px; opacity: 0.9;">The top-level container. Groups related schemas together.</div>
# MAGIC </div>
# MAGIC
# MAGIC <!-- Schema -->
# MAGIC <div style="background: #2574B5; color: white; border-radius: 4px; padding: 18px 24px; text-align: center;">
# MAGIC   <div style="font-size: 16pt; font-weight: 700;">Schema</div>
# MAGIC   <div style="font-size: 14pt; margin-top: 6px; opacity: 0.9;">A collection of related tables, views, and volumes. Organizes data by project or domain.</div>
# MAGIC </div>
# MAGIC
# MAGIC <!-- Tables & Volumes -->
# MAGIC <div style="background: #02A36F; color: white; border-radius: 4px 4px 8px 8px; padding: 18px 24px; text-align: center;">
# MAGIC   <div style="font-size: 16pt; font-weight: 700;">Tables &amp; Volumes</div>
# MAGIC   <div style="font-size: 14pt; margin-top: 6px; opacity: 0.9;">Tables hold structured data (rows and columns). Volumes hold raw files (CSVs, JSON, images).</div>
# MAGIC </div>
# MAGIC
# MAGIC </div>
# MAGIC
# MAGIC </div>
# MAGIC
# MAGIC <!-- Key point callout -->
# MAGIC <div style="margin-top: 20px; padding: 16px 20px; background: #FFF6F4; border: 3px solid #FF5F46; border-radius: 10px;">
# MAGIC   <div style="font-size: 14pt; color: #0b2026; line-height: 1.6;">
# MAGIC     <strong>Your first job as a data engineer:</strong> Find the raw data files in a volume, then turn them into reliable Delta tables that everyone on your team can query.
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
# MAGIC **Catalog → Schema → Tables/Volumes** is the path you'll use every time you work with data in Databricks. This is the three-level namespace that makes Unity Catalog stronger at governance and security.
# MAGIC
# MAGIC - **Catalogs** are the broadest container. In most organizations, you'll have separate catalogs for development, staging, and production, or organized by business unit. In this course, you're working in a pre-configured catalog.
# MAGIC - **Schemas** (also called databases) group related objects together. A schema might hold all the tables for a specific project, team, or data domain. In Databricks, Schemas hold more than just data tables; they also contain volumes, models, and functions.
# MAGIC - **Tables** store structured, queryable data in Delta or Iceberg format (Delta is the default). Once data is in a table, anyone with permission can query it using SQL.
# MAGIC - **Volumes** store raw files before they become tables. Think of a volume as a managed folder where you land CSV files, JSON exports, or other data files that need to be processed.
# MAGIC
# MAGIC This hierarchy is managed by **Unity Catalog**, which also handles permissions. When you create a table inside a schema, Unity Catalog automatically tracks who created it, when, and who has access.
# MAGIC
# MAGIC </details>
# MAGIC
# MAGIC </div>

# COMMAND ----------

# MAGIC %md
# MAGIC
# MAGIC ### Explore: Find your data in the catalog
# MAGIC
# MAGIC Let's start by confirming where we are in the catalog hierarchy, then find the raw data file waiting for us.

# COMMAND ----------

# MAGIC %md
# MAGIC **Step 1:** Run the cell below to confirm your current catalog and schema.

# COMMAND ----------

# MAGIC %sql
# MAGIC USE CATALOG ketancatalog;
# MAGIC USE SCHEMA ketanschema;
# MAGIC
# MAGIC SELECT current_catalog(), current_schema();

# COMMAND ----------

# MAGIC %md
# MAGIC **Step 2:** Let's see what's in our schema. Run the cells below to check for any existing tables and volumes.

# COMMAND ----------

# MAGIC %sql
# MAGIC SHOW TABLES;

# COMMAND ----------

# MAGIC %sql
# MAGIC SHOW VOLUMES;

# COMMAND ----------

# MAGIC %md
# MAGIC **Step 3:** List the files inside the volume. You should see CSV files including `employees.csv`.

# COMMAND ----------

# MAGIC %sql
# MAGIC LIST '/Volumes/ketancatalog/ketanschema/myfiles/';

# COMMAND ----------

# MAGIC %md
# MAGIC **Step 4:** Preview the CSV data without creating a table. The `read_files` function lets you peek at raw file contents directly.

# COMMAND ----------

# MAGIC %sql
# MAGIC SELECT * FROM read_files('/Volumes/ketancatalog/ketanschema/myfiles/employees.csv');

# COMMAND ----------

# MAGIC %md
# MAGIC You should see 4 rows with columns: **ID**, **FirstName**, **Country**, and **Role**. This is raw file data, not stored as a table yet.
# MAGIC
# MAGIC You may also notice a column called **`_rescued_data`** with `null` values. Databricks automatically adds this column when reading files — if any rows don't conform to the inferred schema (wrong data types, extra fields, malformed records), those values are captured here instead of being lost or breaking the read. When all your data is clean, it stays `null`. This is one of the ways Databricks keeps your data safe during ingestion.

# COMMAND ----------

# MAGIC %md
# MAGIC ### Explore: Create a Delta table from the CSV
# MAGIC
# MAGIC Now let's turn that raw CSV into a proper Delta table. The `CREATE TABLE AS SELECT` (CTAS) pattern reads the file and writes the result as a new table in one step.

# COMMAND ----------

# MAGIC %sql
# MAGIC CREATE TABLE IF NOT EXISTS employees
# MAGIC AS SELECT * FROM read_files('/Volumes/ketancatalog/ketanschema/myfiles/employees.csv');

# COMMAND ----------

# MAGIC %md
# MAGIC **Step 5:** Verify the table was created. Run the cell below to query it.

# COMMAND ----------

# MAGIC %sql
# MAGIC use ketancatalog.ketanschema;

# COMMAND ----------

# MAGIC %sql
# MAGIC SELECT * FROM employees;

# COMMAND ----------

# MAGIC %md
# MAGIC Same 4 rows, but now they're stored as a **Delta table** with a transaction log tracking every change. You can also verify this in **Catalog Explorer**: click **Catalog** in the left sidebar, expand your catalog and schema, and you should see the `employees` table listed under **Tables**. 
# MAGIC
# MAGIC Databricks tables use Delta format by default, but Databricks also natively supports Apache Iceberg™ as a table format. Both are open source. In this course, we use Delta, but if your organization uses Iceberg, you can create and query Iceberg tables in the same catalog. You can learn more by reading our [documentation on the topic](https://docs.databricks.com/aws/en/delta/uniform).

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
# MAGIC       <li>Navigated the Unity Catalog hierarchy (catalog → schema → volume)</li>
# MAGIC       <li>Previewed raw CSV data using <code>read_files</code></li>
# MAGIC       <li>Created your first Delta table using <code>CREATE TABLE AS SELECT</code></li>
# MAGIC       <li>Verified the table in both SQL and Catalog Explorer</li>
# MAGIC     </ul>
# MAGIC   </div>
# MAGIC </div>
# MAGIC </div>
