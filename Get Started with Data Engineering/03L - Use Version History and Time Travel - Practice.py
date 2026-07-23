# Databricks notebook source
# MAGIC %md-sandbox
# MAGIC
# MAGIC <div style="max-width: 1000px; margin: 0 auto; font-family: sans-serif;">
# MAGIC
# MAGIC <div style="background: #02A36F; color: white; border-radius: 8px; padding: 28px 32px; text-align: center; position: relative;">
# MAGIC   <div style="font-size: 14pt; font-weight: 600; text-transform: uppercase; letter-spacing: 1px; opacity: 0.85; margin-bottom: 8px;">Practice</div>
# MAGIC   <div style="font-size: 24pt; font-weight: 700; line-height: 1.3;">Use Version History and Time Travel</div>
# MAGIC   <div style="font-size: 14pt; margin-top: 12px; opacity: 0.9;">Explore the version history of the <code>new_employees</code> table and query its previous states.</div>
# MAGIC </div>
# MAGIC
# MAGIC </div>

# COMMAND ----------


# MAGIC %md
# MAGIC **Where we left off:** In Lesson 2 Practice, you modified the `new_employees` table with INSERT, UPDATE, and DELETE. It should have a version history with 4 versions (0 through 3). Let's confirm the current state.
# MAGIC
# MAGIC *Prerequisite: You must complete **Practice 01L** and **Practice 02L** before starting this practice. The version history explored here is built by those exercises.*

# COMMAND ----------

# MAGIC %sql
# MAGIC USE CATALOG dbacademy;
# MAGIC USE SCHEMA get_started_de;
# MAGIC
# MAGIC SELECT * FROM new_employees;

# COMMAND ----------

# MAGIC %md
# MAGIC ### Task 1: View the version history
# MAGIC
# MAGIC Use `DESCRIBE HISTORY` to see the full change log for `new_employees`.

# COMMAND ----------

# MAGIC %sql
# MAGIC -- TODO: Show the version history of new_employees
# MAGIC <FILL_IN>

# COMMAND ----------

# MAGIC %md-sandbox
# MAGIC <details>
# MAGIC <summary>Hint</summary>
# MAGIC
# MAGIC <pre><code>DESCRIBE HISTORY new_employees;</code></pre>
# MAGIC
# MAGIC </details>

# COMMAND ----------

# MAGIC %md
# MAGIC Look at the **operation** column for each version. Can you match each version to what you did in Practice 2?
# MAGIC - Version 0 should be `CREATE TABLE`
# MAGIC - Version 1 should be `WRITE` (the INSERT)
# MAGIC - Version 2 should be `UPDATE`
# MAGIC - Version 3 should be `DELETE`

# COMMAND ----------

# MAGIC %md
# MAGIC ### Task 2: Query the original version
# MAGIC
# MAGIC Query `new_employees` as it was at **version 0** — right after it was created from `employees2.csv`, before any modifications.

# COMMAND ----------

# MAGIC %sql
# MAGIC -- TODO: Query new_employees at version 0
# MAGIC <FILL_IN>

# COMMAND ----------

# MAGIC %md-sandbox
# MAGIC <details>
# MAGIC <summary>Hint</summary>
# MAGIC
# MAGIC <pre><code>SELECT * FROM new_employees VERSION AS OF 0;</code></pre>
# MAGIC
# MAGIC </details>

# COMMAND ----------

# MAGIC %md
# MAGIC You should see the original 2 rows: Maria as `Data Engineer` and Aiden as `Data Analyst`. No Priya, and no role changes yet.

# COMMAND ----------

# MAGIC %md
# MAGIC ### Task 3: Find a specific change
# MAGIC
# MAGIC In Practice 2, you updated Aiden's role. Query the version **right after the INSERT but before the UPDATE** to see Aiden's original role alongside Priya's row.

# COMMAND ----------

# MAGIC %sql
# MAGIC -- TODO: Query the version that has all 3 rows with original roles (after INSERT, before UPDATE)
# MAGIC <FILL_IN>

# COMMAND ----------

# MAGIC %md-sandbox
# MAGIC <details>
# MAGIC <summary>Hint</summary>
# MAGIC
# MAGIC The INSERT was version 1. Query that version:
# MAGIC <pre><code>SELECT * FROM new_employees VERSION AS OF 1;</code></pre>
# MAGIC
# MAGIC </details>

# COMMAND ----------

# MAGIC %md
# MAGIC You should see 3 rows: Maria, Aiden (still `Data Analyst`), and Priya. This is the state between the INSERT and the UPDATE.

# COMMAND ----------

# MAGIC %md
# MAGIC ### Task 4: Compare current vs. original
# MAGIC
# MAGIC Write a query that shows the row count for both the **current version** and **version 0** of `new_employees`. Use UNION ALL to combine the results.

# COMMAND ----------

# MAGIC %sql
# MAGIC -- TODO: Compare row counts between current and version 0
# MAGIC <FILL_IN>

# COMMAND ----------

# MAGIC %md-sandbox
# MAGIC <details>
# MAGIC <summary>Hint</summary>
# MAGIC
# MAGIC <pre><code>SELECT 'Current' AS version, COUNT(*) AS row_count FROM new_employees
# MAGIC UNION ALL
# MAGIC SELECT 'Version 0', COUNT(*) FROM new_employees VERSION AS OF 0;</code></pre>
# MAGIC
# MAGIC </details>

# COMMAND ----------

# MAGIC %md
# MAGIC Both should show **2 rows** — you started with 2, added 1, then deleted 1. The data is the same size but the content is different (Aiden's role changed). This is why comparing row counts alone isn't enough; sometimes you need to compare the actual data.

# COMMAND ----------

# MAGIC %md
# MAGIC ### Task 5: Try the shorthand syntax
# MAGIC
# MAGIC Query version 0 of `new_employees` using the `@v` shorthand instead of `VERSION AS OF`.

# COMMAND ----------

# MAGIC %sql
# MAGIC -- TODO: Query version 0 using the @v shorthand
# MAGIC <FILL_IN>

# COMMAND ----------

# MAGIC %md-sandbox
# MAGIC <details>
# MAGIC <summary>Hint</summary>
# MAGIC
# MAGIC <pre><code>SELECT * FROM new_employees@v0;</code></pre>
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
# MAGIC       <li>Inspected the full change log with <code>DESCRIBE HISTORY</code></li>
# MAGIC       <li>Queried previous versions to see data before it was modified</li>
# MAGIC       <li>Compared row counts across versions</li>
# MAGIC       <li>Used the <code>@v</code> shorthand for time travel queries</li>
# MAGIC     </ul>
# MAGIC   </div>
# MAGIC </div>
# MAGIC </div>

# COMMAND ----------

# MAGIC %md-sandbox
# MAGIC
# MAGIC <!-- CHECKPOINT: Lessons 1-3 -->
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
# MAGIC     <p>Over Lessons 1 through 3, you:</p>
# MAGIC     <ul style="padding-left: 20px; margin: 8px 0;">
# MAGIC       <li>Navigated the Unity Catalog hierarchy to find raw data files in a volume</li>
# MAGIC       <li>Created Delta tables from CSV files using <code>CREATE TABLE AS SELECT</code></li>
# MAGIC       <li>Modified data with <code>INSERT</code>, <code>UPDATE</code>, and <code>DELETE</code></li>
# MAGIC       <li>Viewed the full change log with <code>DESCRIBE HISTORY</code></li>
# MAGIC       <li>Queried previous versions of your data using time travel</li>
# MAGIC     </ul>
# MAGIC     <p>You now have the foundational skills for working with Delta tables: creating them from raw files, modifying their contents, and auditing every change.</p>
# MAGIC   </div>
# MAGIC </div>
# MAGIC
# MAGIC <div style="margin-top: 16px; padding: 16px 20px; background: #F8F9FC; border-left: 4px solid #1B5162; border-radius: 6px;">
# MAGIC   <div style="font-size: 14pt; color: #0b2026; line-height: 1.6;">
# MAGIC     <strong>Quick self-check:</strong> If a teammate accidentally deleted rows from a table, could you use time travel to see what the data looked like before the delete? Could you explain how to find the right version number?
# MAGIC   </div>
# MAGIC </div>
# MAGIC
