# Databricks notebook source
# MAGIC %md-sandbox
# MAGIC
# MAGIC <div style="max-width: 1000px; margin: 0 auto; font-family: sans-serif;">
# MAGIC
# MAGIC <div style="background: #1B5162; color: white; border-radius: 8px; padding: 28px 32px; text-align: center; position: relative;">
# MAGIC   <div style="font-size: 14pt; font-weight: 600; text-transform: uppercase; letter-spacing: 1px; opacity: 0.85; margin-bottom: 8px;">Lesson 3</div>
# MAGIC   <div style="font-size: 24pt; font-weight: 700; line-height: 1.3;">Explore Version History and Time Travel</div>
# MAGIC   <div style="font-size: 14pt; margin-top: 12px; opacity: 0.9;">View a Delta table's change log and query data from any previous version.</div>
# MAGIC </div>
# MAGIC
# MAGIC </div>

# COMMAND ----------


# MAGIC %md
# MAGIC **Where we left off:** In Lessons 1 and 2, we created and modified the `employees` table with INSERT, UPDATE, and DELETE. Each operation created a new version. Let's start by looking at the current state of the table.

# COMMAND ----------

# MAGIC %sql
# MAGIC USE CATALOG dbacademy;
# MAGIC USE SCHEMA get_started_de;
# MAGIC
# MAGIC SELECT * FROM employees;

# COMMAND ----------

# MAGIC %md-sandbox
# MAGIC
# MAGIC <!-- LEARN: Version History and Time Travel -->
# MAGIC <!-- Template: 2-card-colored-header-guidance -->
# MAGIC
# MAGIC <div style="max-width: 950px; margin: 0 auto; font-family: sans-serif; color: #0b2026;">
# MAGIC
# MAGIC <div style="font-size: 20pt; font-weight: 700; color: #0b2026; margin-bottom: 6px;">Every Change is Recorded. Every Version is Queryable.</div>
# MAGIC <div style="font-size: 14pt; color: #5A6F77; margin-bottom: 24px;">Delta Lake automatically maintains a transaction log that records every operation performed on a table. You can inspect this log and query data as it existed at any point in the past.</div>
# MAGIC
# MAGIC <div style="display: flex; gap: 20px; justify-content: center;">
# MAGIC
# MAGIC <!-- Card 1: DESCRIBE HISTORY -->
# MAGIC <div style="flex: 1; border: 2px solid #e0e0e0; border-radius: 12px; overflow: hidden; background: white;">
# MAGIC   <div style="background: #4299E0; color: white; padding: 14px 20px; text-align: center;">
# MAGIC     <div style="font-size: 18pt; font-weight: bold;">DESCRIBE HISTORY</div>
# MAGIC   </div>
# MAGIC   <div style="padding: 18px 20px;">
# MAGIC     <div style="font-size: 14pt; color: #555; line-height: 1.6; margin-bottom: 14px;">
# MAGIC       Shows the full change log for a table: every version number, timestamp, operation type, and who made the change.
# MAGIC     </div>
# MAGIC     <div style="background: rgba(66,153,224,0.10); border-left: 4px solid #4299E0; padding: 10px 12px; border-radius: 6px; font-size: 14pt;">
# MAGIC       <strong>Use when:</strong> You need to audit what happened to a table, debug unexpected data, or find a version number to restore.
# MAGIC     </div>
# MAGIC   </div>
# MAGIC </div>
# MAGIC
# MAGIC <!-- Card 2: Time Travel -->
# MAGIC <div style="flex: 1; border: 2px solid #e0e0e0; border-radius: 12px; overflow: hidden; background: white;">
# MAGIC   <div style="background: #00A972; color: white; padding: 14px 20px; text-align: center;">
# MAGIC     <div style="font-size: 18pt; font-weight: bold;">VERSION AS OF / TIMESTAMP AS OF</div>
# MAGIC   </div>
# MAGIC   <div style="padding: 18px 20px;">
# MAGIC     <div style="font-size: 14pt; color: #555; line-height: 1.6; margin-bottom: 14px;">
# MAGIC       Query the table as it existed at a specific version number or point in time. The current table is unchanged; you're just reading the old data.
# MAGIC     </div>
# MAGIC     <div style="background: rgba(0,169,114,0.10); border-left: 4px solid #00A972; padding: 10px 12px; border-radius: 6px; font-size: 14pt;">
# MAGIC       <strong>Use when:</strong> You need to see what data looked like before a change, compare versions, or recover accidentally deleted rows.
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
# MAGIC **How Delta Lake versioning works**
# MAGIC
# MAGIC - Every time you run a DML statement (INSERT, UPDATE, DELETE, MERGE) or a DDL statement (CREATE TABLE, ALTER TABLE), Delta Lake writes a new entry to the table's **transaction log**.
# MAGIC - Each entry is a **version**, starting at 0 (the initial CREATE TABLE) and incrementing by 1 for each subsequent operation.
# MAGIC - The transaction log records the operation type, timestamp, user, and which data files were added or removed.
# MAGIC - When you query a table normally (`SELECT * FROM employees`), you always get the latest version.
# MAGIC - Time travel lets you read any previous version by adding `VERSION AS OF <number>` or `TIMESTAMP AS OF '<datetime>'` to your query.
# MAGIC - Old versions are retained based on the table's retention policy (default: 30 days). After that, the underlying data files may be cleaned up by the `VACUUM` command.
# MAGIC
# MAGIC **Why this matters**
# MAGIC
# MAGIC - **Auditing:** You can prove exactly what changed, when, and who did it.
# MAGIC - **Debugging:** If a dashboard suddenly shows wrong numbers, you can compare the current version to yesterday's version to find the bad write.
# MAGIC - **Recovery:** If someone accidentally deletes rows, you can query the version before the delete and use it to restore the data.
# MAGIC
# MAGIC </details>
# MAGIC
# MAGIC </div>

# COMMAND ----------

# MAGIC %md
# MAGIC ### Explore: View the full version history
# MAGIC
# MAGIC Let's inspect every change that's been made to the `employees` table since it was created.

# COMMAND ----------

# MAGIC %sql
# MAGIC DESCRIBE HISTORY employees;

# COMMAND ----------

# MAGIC %md
# MAGIC You should see multiple versions, each with:
# MAGIC - **version** — the version number, starting at 0
# MAGIC - **timestamp** — when the operation happened
# MAGIC - **operation** — what type of change it was (CREATE TABLE, WRITE, UPDATE, DELETE)
# MAGIC - **userName** — who made the change
# MAGIC
# MAGIC Take a moment to match each version to the operations you ran in Lesson 2.

# COMMAND ----------

# MAGIC %md
# MAGIC ### Explore: Query a previous version
# MAGIC
# MAGIC Let's go back in time. Version 0 is the original table as it was created in Lesson 1 — before any INSERT, UPDATE, or DELETE operations.

# COMMAND ----------

# MAGIC %sql
# MAGIC SELECT * FROM employees VERSION AS OF 0;

# COMMAND ----------

# MAGIC %md
# MAGIC You should see just the **original 4 rows** from the CSV file. No Maria, no Aiden, no changes. This is exactly what the table looked like right after `CREATE TABLE` in Lesson 1.

# COMMAND ----------

# MAGIC %md
# MAGIC Now let's check version 1 — right after the INSERT (before the UPDATE and DELETE).

# COMMAND ----------

# MAGIC %sql
# MAGIC SELECT * FROM employees VERSION AS OF 1;

# COMMAND ----------

# MAGIC %md
# MAGIC You should see **6 rows**: the original 4 plus Maria and Aiden. Maria's role is still `Data Engineer` (not yet updated) and Aiden is still present (not yet deleted).

# COMMAND ----------

# MAGIC %md
# MAGIC ### Explore: Compare versions side by side
# MAGIC
# MAGIC A common pattern is comparing the current version to a previous one. Let's count how many rows exist in the current version versus version 0.

# COMMAND ----------

# MAGIC %sql
# MAGIC SELECT 'Current' AS version, COUNT(*) AS row_count FROM employees
# MAGIC UNION ALL
# MAGIC SELECT 'Version 0', COUNT(*) FROM employees VERSION AS OF 0;

# COMMAND ----------

# MAGIC %md
# MAGIC This pattern is useful for debugging. If a table suddenly has more or fewer rows than expected, you can compare against a known-good version to identify which operation caused the change.

# COMMAND ----------

# MAGIC %md
# MAGIC ### Explore: Use the shorthand syntax
# MAGIC
# MAGIC Databricks also supports a shorter syntax using `@v` followed by the version number.

# COMMAND ----------

# MAGIC %sql
# MAGIC SELECT * FROM employees@v0;

# COMMAND ----------

# MAGIC %md
# MAGIC This returns the same result as `VERSION AS OF 0`. Use whichever syntax you find more readable.

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
# MAGIC       <li>Viewed the full change log with <code>DESCRIBE HISTORY</code></li>
# MAGIC       <li>Queried previous versions with <code>VERSION AS OF</code></li>
# MAGIC       <li>Compared row counts across versions to detect changes</li>
# MAGIC       <li>Used the <code>@v</code> shorthand syntax for time travel</li>
# MAGIC     </ul>
# MAGIC   </div>
# MAGIC </div>
# MAGIC </div>
