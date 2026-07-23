# Databricks notebook source
# MAGIC %md-sandbox
# MAGIC
# MAGIC <div style="max-width: 1000px; margin: 0 auto; font-family: sans-serif;">
# MAGIC
# MAGIC <div style="background: #1B5162; color: white; border-radius: 8px; padding: 28px 32px; text-align: center; position: relative;">
# MAGIC   <div style="font-size: 14pt; font-weight: 600; text-transform: uppercase; letter-spacing: 1px; opacity: 0.85; margin-bottom: 8px;">Lesson 7</div>
# MAGIC   <div style="font-size: 24pt; font-weight: 700; line-height: 1.3;">Automate Your Pipeline with a LakeFlow Job</div>
# MAGIC   <div style="font-size: 14pt; margin-top: 12px; opacity: 0.9;">Create a multi-task LakeFlow Job that orchestrates the Bronze → Silver → Gold pipeline with task dependencies, and monitor its execution.</div>
# MAGIC </div>
# MAGIC
# MAGIC </div>

# COMMAND ----------


# MAGIC %md
# MAGIC **In this lesson:** In Lesson 6, you learned how to build the full Medallion Architecture pipeline manually: Bronze, Silver, Gold. In this lesson, you'll automate it so it runs on its own using Lakeflow Jobs.

# COMMAND ----------

# MAGIC %md-sandbox
# MAGIC
# MAGIC <!-- LEARN: LakeFlow Jobs -->
# MAGIC <!-- Template: source-process-output-flow (adapted) -->
# MAGIC
# MAGIC <div style="max-width: 900px; margin: 0 auto; font-family: sans-serif;">
# MAGIC
# MAGIC <div style="font-size: 20pt; font-weight: 700; color: #0b2026; margin-bottom: 6px;">LakeFlow Jobs: Orchestrate Your Pipeline</div>
# MAGIC <div style="font-size: 14pt; color: #5A6F77; margin-bottom: 24px;">A LakeFlow Job runs one or more notebooks as tasks, with dependencies between them. You define what runs, in what order, and on what schedule.</div>
# MAGIC
# MAGIC <div style="display: flex; justify-content: center; align-items: center; gap: 16px;">
# MAGIC
# MAGIC   <!-- Task 1 -->
# MAGIC   <div style="flex: 0 0 260px; background: #F9F7F4; border-radius: 10px; padding: 18px; box-shadow: 0 2px 8px rgba(27,49,57,0.08); text-align: center; border-top: 6px solid #CD7F32;">
# MAGIC     <div style="font-size: 16pt; font-weight: 700; margin-bottom: 8px;">Task 1: Setup + Bronze</div>
# MAGIC     <div style="font-size: 14pt; color: #5A6F77;">Creates the volume, loads CSV files into the Bronze table</div>
# MAGIC   </div>
# MAGIC
# MAGIC   <!-- Arrow -->
# MAGIC   <div style="font-size: 28pt; color: #618794;">→</div>
# MAGIC
# MAGIC   <!-- Task 2 -->
# MAGIC   <div style="flex: 0 0 260px; background: #F9F7F4; border-radius: 10px; padding: 18px; box-shadow: 0 2px 8px rgba(27,49,57,0.08); text-align: center; border-top: 6px solid #FFAB00;">
# MAGIC     <div style="font-size: 16pt; font-weight: 700; margin-bottom: 8px;">Task 2: Silver + Gold</div>
# MAGIC     <div style="font-size: 14pt; color: #5A6F77;">Transforms Bronze → Silver, aggregates Silver → Gold</div>
# MAGIC   </div>
# MAGIC
# MAGIC </div>
# MAGIC
# MAGIC <!-- Connector line -->
# MAGIC <div style="margin: 14px auto 0 auto; width: 60%; height: 4px; background: #1B5162; border-radius: 2px;"></div>
# MAGIC
# MAGIC <!-- Key point -->
# MAGIC <div style="margin-top: 18px; padding: 16px 20px; background: #FFF6F4; border: 3px solid #FF5F46; border-radius: 10px;">
# MAGIC   <div style="font-size: 14pt; color: #0b2026; line-height: 1.6;">
# MAGIC     <strong>The dependency arrow means Task 2 only runs if Task 1 succeeds.</strong> If Bronze fails, Silver and Gold won't run with stale or missing data. This is how production pipelines stay reliable.
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
# MAGIC **What LakeFlow Jobs give you**
# MAGIC
# MAGIC - **Task dependencies:** Define which tasks must complete before others start. The job visualizes this as a directed acyclic graph (DAG).
# MAGIC - **Scheduling:** Run on a cron schedule (every hour, daily at 6am), on file arrival (new files land in a volume), or on table updates.
# MAGIC - **Monitoring:** Each run shows status per task (Pending → Running → Succeeded/Failed), duration, and output.
# MAGIC - **Alerting:** Configure email or Slack notifications on failure so your team knows immediately when a pipeline breaks.
# MAGIC
# MAGIC **Jobs vs. notebooks**
# MAGIC
# MAGIC - Running a notebook interactively is great for development and exploration. But production pipelines need to run automatically, on a schedule, without someone clicking "Run All."
# MAGIC - A LakeFlow Job wraps your notebooks into an automated, monitored, and schedulable workflow. The notebooks are the same ones you developed interactively.
# MAGIC
# MAGIC </details>
# MAGIC
# MAGIC </div>

# COMMAND ----------

# MAGIC %md
# MAGIC ### Explore: Locate the task notebooks
# MAGIC
# MAGIC Two task notebooks have been pre-loaded in the `Includes` folder of this project. These are the notebooks the job will execute:
# MAGIC
# MAGIC - **Task 1 - Setup - Bronze** — Sets up the environment and loads CSV files into a Bronze table
# MAGIC - **Task 2 - Silver - Gold** — Transforms Bronze into Silver and aggregates into Gold
# MAGIC
# MAGIC You can open them from the file browser to review their contents before creating the job.

# COMMAND ----------

# MAGIC %md
# MAGIC ### Explore: Create the LakeFlow Job
# MAGIC
# MAGIC Now you'll create a job that runs these two notebooks in sequence.
# MAGIC
# MAGIC **Follow these steps:**
# MAGIC
# MAGIC 1. In the left sidebar, right-click **Jobs & Pipelines** and select **Open in new tab**
# MAGIC 2. Click **Create** and select **Job**
# MAGIC 3. Name your job (e.g., `yourname-bronze-silver-gold-pipeline`)
# MAGIC
# MAGIC **Configure Task 1:**
# MAGIC 4. Set the task name to **Setup-Bronze**
# MAGIC 5. Type: **Notebook**
# MAGIC 6. Source: **Workspace**
# MAGIC 7. Path: Navigate to your project folder → `Includes` → select **Task 1 - Setup - Bronze**
# MAGIC 8. Compute: **Serverless**
# MAGIC 9. Click **Create task**
# MAGIC
# MAGIC **Configure Task 2:**
# MAGIC 10. Click **Add task** → **Notebook**
# MAGIC 11. Set the task name to **Silver-Gold**
# MAGIC 12. Path: Navigate to `Includes` → select **Task 2 - Silver - Gold**
# MAGIC 13. Compute: **Serverless**
# MAGIC 14. Depends on: **Setup-Bronze**
# MAGIC 15. Run if dependencies: **All succeeded**
# MAGIC 16. Click **Create task**
# MAGIC
# MAGIC You should see a visual DAG (directed acyclic graph) with a dependency arrow from Setup-Bronze to Silver-Gold.

# COMMAND ----------

# MAGIC %md
# MAGIC ### Explore: Browse scheduling options
# MAGIC
# MAGIC Before running the job, take a moment to explore what scheduling options are available:
# MAGIC
# MAGIC 1. In the job editor, find **Schedules & Triggers** on the right side
# MAGIC 2. Click **Add trigger**
# MAGIC 3. Browse the options: **Scheduled** (cron), **File arrival**, **Table updates**, **Continuous**
# MAGIC 4. Click **Cancel** — we'll run the job manually for now
# MAGIC
# MAGIC In production, you'd schedule this to run daily or trigger it when new files arrive in the volume.

# COMMAND ----------

# MAGIC %md
# MAGIC ### Explore: Run the job
# MAGIC
# MAGIC 1. Click **Run now** in the top right
# MAGIC 2. Click the **Runs** tab to watch the execution
# MAGIC 3. You'll see each task progress: **Pending** → **Running** → **Succeeded**
# MAGIC 4. The job typically takes 2-5 minutes to complete
# MAGIC
# MAGIC Once both tasks show **Succeeded**, click either task to see its output.

# COMMAND ----------

# MAGIC %md
# MAGIC ### Explore: Verify the results
# MAGIC
# MAGIC After the job completes, verify that the pipeline created the expected tables. The job creates tables with a `_job` suffix to avoid overwriting your manual tables from Lesson 6.

# COMMAND ----------

# MAGIC %sql
# MAGIC USE CATALOG dbacademy;
# MAGIC USE SCHEMA get_started_de;
# MAGIC
# MAGIC SELECT * FROM current_employees_bronze_job;

# COMMAND ----------

# MAGIC %sql
# MAGIC SELECT * FROM current_employees_silver_job;

# COMMAND ----------

# MAGIC %sql
# MAGIC SELECT * FROM total_roles_gold_job;

# COMMAND ----------

# MAGIC %md
# MAGIC The same Bronze → Silver → Gold pipeline you built manually in Lesson 6, now running automatically as an orchestrated job.

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
# MAGIC       <li>Created a <strong>LakeFlow Job</strong> with two tasks and a dependency</li>
# MAGIC       <li>Explored scheduling options (cron, file arrival, table updates)</li>
# MAGIC       <li>Ran the job and monitored each task's execution</li>
# MAGIC       <li>Verified the automated pipeline produced the same Bronze → Silver → Gold results</li>
# MAGIC     </ul>
# MAGIC   </div>
# MAGIC </div>
# MAGIC </div>
