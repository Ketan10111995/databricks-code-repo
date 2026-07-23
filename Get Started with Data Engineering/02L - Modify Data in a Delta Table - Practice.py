# Databricks notebook source
# MAGIC %md-sandbox
# MAGIC
# MAGIC <div style="max-width: 1000px; margin: 0 auto; font-family: sans-serif;">
# MAGIC
# MAGIC <div style="background: #02A36F; color: white; border-radius: 8px; padding: 28px 32px; text-align: center; position: relative;">
# MAGIC   <div style="font-size: 14pt; font-weight: 600; text-transform: uppercase; letter-spacing: 1px; opacity: 0.85; margin-bottom: 8px;">Practice</div>
# MAGIC   <div style="font-size: 24pt; font-weight: 700; line-height: 1.3;">Modify Data in a Delta Table</div>
# MAGIC   <div style="font-size: 14pt; margin-top: 12px; opacity: 0.9;">Practice INSERT, UPDATE, and DELETE on the <code>new_employees</code> table you created in Practice 1.</div>
# MAGIC </div>
# MAGIC
# MAGIC </div>

# COMMAND ----------


# MAGIC %md
# MAGIC **Where we left off:** In Lesson 1's Practice, you created a `new_employees` table from `employees2.csv`. It should have 2 rows (Maria and Aiden). Let's confirm.
# MAGIC
# MAGIC *Prerequisite: You must complete **Practice 01L** before starting this activity. The `new_employees` table is created there.*

# COMMAND ----------

# MAGIC %sql
# MAGIC USE CATALOG dbacademy;
# MAGIC USE SCHEMA get_started_de;
# MAGIC
# MAGIC SELECT * FROM new_employees;

# COMMAND ----------

# MAGIC %md
# MAGIC ### Task 1: Insert a new employee
# MAGIC
# MAGIC Add a new row to `new_employees` with the following values:
# MAGIC - **ID:** 7
# MAGIC - **FirstName:** Priya
# MAGIC - **Country:** India
# MAGIC - **Role:** Data Engineer

# COMMAND ----------

# MAGIC %sql
# MAGIC -- TODO: Insert Priya into the new_employees table
# MAGIC <FILL_IN>

# COMMAND ----------

# MAGIC %md-sandbox
# MAGIC <details>
# MAGIC <summary>Hint</summary>
# MAGIC
# MAGIC <pre><code>INSERT INTO new_employees (ID, FirstName, Country, Role) VALUES (7, 'Priya', 'India', 'Data Engineer');</code></pre>
# MAGIC
# MAGIC </details>

# COMMAND ----------

# MAGIC %md
# MAGIC Verify the insert worked. You should see **3 rows**.

# COMMAND ----------

# MAGIC %sql
# MAGIC SELECT * FROM new_employees;

# COMMAND ----------

# MAGIC %md
# MAGIC ### Task 2: Update a role
# MAGIC
# MAGIC Aiden has been promoted. Update his role from `Data Analyst` to `Senior Data Analyst`.

# COMMAND ----------

# MAGIC %sql
# MAGIC -- TODO: Update Aiden's role to Senior Data Analyst
# MAGIC <FILL_IN>

# COMMAND ----------

# MAGIC %md-sandbox
# MAGIC <details>
# MAGIC <summary>Hint</summary>
# MAGIC
# MAGIC <pre><code>UPDATE new_employees
# MAGIC SET Role = 'Senior Data Analyst'
# MAGIC WHERE FirstName = 'Aiden';</code></pre>
# MAGIC
# MAGIC </details>

# COMMAND ----------

# MAGIC %md
# MAGIC Verify the update. Aiden's role should now show `Senior Data Analyst`.

# COMMAND ----------

# MAGIC %sql
# MAGIC SELECT * FROM new_employees WHERE FirstName = 'Aiden';

# COMMAND ----------

# MAGIC %md
# MAGIC ### Task 3: Delete a row
# MAGIC
# MAGIC Priya accepted another offer and won't be joining after all. Remove her record from the table.

# COMMAND ----------

# MAGIC %sql
# MAGIC -- TODO: Delete Priya from the new_employees table
# MAGIC <FILL_IN>

# COMMAND ----------

# MAGIC %md-sandbox
# MAGIC <details>
# MAGIC <summary>Hint</summary>
# MAGIC
# MAGIC <pre><code>DELETE FROM new_employees
# MAGIC WHERE FirstName = 'Priya';</code></pre>
# MAGIC
# MAGIC </details>

# COMMAND ----------

# MAGIC %md
# MAGIC Verify the delete. You should be back to **2 rows**.

# COMMAND ----------

# MAGIC %sql
# MAGIC SELECT * FROM new_employees;

# COMMAND ----------

# MAGIC %md
# MAGIC ### Task 4: Check the version history
# MAGIC
# MAGIC Use `DESCRIBE HISTORY` to see all the changes you just made to `new_employees`.

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
# MAGIC You should see 4 versions: the original `CREATE TABLE` (version 0), your INSERT (version 1), UPDATE (version 2), and DELETE (version 3). Every change is tracked automatically.

# COMMAND ----------

# MAGIC %md-sandbox
# MAGIC
# MAGIC <div style="max-width: 900px; margin: 0 auto; font-family: sans-serif;">
# MAGIC <div style="margin-top: 10px; padding: 18px 24px; background: #FFF6F4; border: 3px solid #FF5F46; border-radius: 10px;">
# MAGIC   <div style="font-size: 14pt; color: #0b2026; line-height: 1.6;">
# MAGIC     <div style="font-weight: 700; margin-bottom: 8px;">Nice work! You just:</div>
# MAGIC     <ul style="padding-left: 20px; margin: 0;">
# MAGIC       <li>Added a row with <code>INSERT INTO</code></li>
# MAGIC       <li>Changed a value with <code>UPDATE ... SET ... WHERE</code></li>
# MAGIC       <li>Removed a row with <code>DELETE FROM ... WHERE</code></li>
# MAGIC       <li>Confirmed all operations are versioned with <code>DESCRIBE HISTORY</code></li>
# MAGIC     </ul>
# MAGIC     <div style="margin-top: 12px;">Both your tables now have a full version history.</div>
# MAGIC   </div>
# MAGIC </div>
# MAGIC </div>
