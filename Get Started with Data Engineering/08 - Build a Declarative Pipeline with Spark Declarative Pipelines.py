# Databricks notebook source

# MAGIC %md-sandbox
# MAGIC
# MAGIC <div style="max-width: 1000px; margin: 0 auto; font-family: sans-serif;">
# MAGIC
# MAGIC <div style="background: #1B5162; color: white; border-radius: 8px; padding: 28px 32px; text-align: center; position: relative;">
# MAGIC   <div style="font-size: 14pt; font-weight: 600; text-transform: uppercase; letter-spacing: 1px; opacity: 0.85; margin-bottom: 8px;">Bonus Lesson</div>
# MAGIC   <div style="font-size: 24pt; font-weight: 700; line-height: 1.3;">Build a Declarative Pipeline with Spark Declarative Pipelines</div>
# MAGIC   <div style="font-size: 14pt; margin-top: 12px; opacity: 0.9;">Rebuild the Bronze → Silver → Gold pipeline declaratively — define what you want, and let Databricks figure out how to run it.</div>
# MAGIC </div>
# MAGIC
# MAGIC </div>

# COMMAND ----------

# MAGIC %md-sandbox
# MAGIC
# MAGIC <div style="max-width: 900px; margin: 0 auto; font-family: sans-serif;">
# MAGIC <div style="padding: 18px 24px; background: #E3F2FD; border: 3px solid #4299E0; border-radius: 10px;">
# MAGIC   <div style="font-size: 14pt; color: #0b2026; line-height: 1.6;">
# MAGIC     <div style="font-weight: 700; margin-bottom: 8px; font-size: 16pt;">This notebook works differently</div>
# MAGIC     <p>Unlike the previous lessons, you <strong>cannot run these SQL cells interactively</strong>. This notebook is designed to be executed by the <strong>Spark Declarative Pipelines</strong> engine.</p>
# MAGIC     <p>You will:</p>
# MAGIC     <ol style="padding-left: 20px; margin: 8px 0;">
# MAGIC       <li><strong>Read</strong> through the lesson content and SQL definitions below</li>
# MAGIC       <li><strong>Create</strong> an ETL Pipeline in the Jobs &amp; Pipelines UI, pointing at this notebook</li>
# MAGIC       <li><strong>Start</strong> the pipeline and watch it build your tables automatically</li>
# MAGIC       <li><strong>Explore</strong> the results in the Practice notebook</li>
# MAGIC     </ol>
# MAGIC   </div>
# MAGIC </div>
# MAGIC </div>

# COMMAND ----------

# MAGIC %md
# MAGIC **In this lesson:** In Lesson 7, you automated the Bronze → Silver → Gold pipeline using a LakeFlow Job with two task notebooks. It worked, but you had to write the orchestration yourself: create the empty tables, run COPY INTO, define the transformations, manage task dependencies.
# MAGIC
# MAGIC What if you could just *describe* the tables you want, and let Databricks handle the rest? Let's find out!

# COMMAND ----------

# MAGIC %md-sandbox
# MAGIC
# MAGIC <!-- LEARN: Imperative vs Declarative -->
# MAGIC <!-- Template: 2-card-colored-header-guidance -->
# MAGIC
# MAGIC <div style="max-width: 950px; margin: 0 auto; font-family: sans-serif; color: #0b2026;">
# MAGIC
# MAGIC <div style="font-size: 20pt; font-weight: 700; color: #0b2026; margin-bottom: 6px;">Imperative vs. Declarative Pipelines</div>
# MAGIC <div style="font-size: 14pt; color: #5A6F77; margin-bottom: 24px;">Two approaches to building the same pipeline — one tells Databricks <em>how</em>, the other tells Databricks <em>what</em>.</div>
# MAGIC
# MAGIC <div style="display: flex; gap: 20px; justify-content: center;">
# MAGIC
# MAGIC <!-- Card 1: Imperative -->
# MAGIC <div style="flex: 1; border: 2px solid #e0e0e0; border-radius: 12px; overflow: hidden; background: white;">
# MAGIC   <div style="background: #90A5B1; color: white; padding: 14px 20px; text-align: center;">
# MAGIC     <div style="font-size: 18pt; font-weight: bold;">Imperative (Lessons 6-7)</div>
# MAGIC   </div>
# MAGIC   <div style="padding: 18px 20px;">
# MAGIC     <div style="font-size: 14pt; color: #555; line-height: 1.6; margin-bottom: 14px;">
# MAGIC       You wrote step-by-step instructions: create an empty table, run COPY INTO, create the Silver table from Bronze, create a temp view, insert into Gold. You managed the order and dependencies yourself.
# MAGIC     </div>
# MAGIC     <div style="background: rgba(144,165,177,0.15); border-left: 4px solid #90A5B1; padding: 10px 12px; border-radius: 6px; font-size: 14pt;">
# MAGIC       <strong>You said:</strong> "First do this, then do that, then do the other thing."
# MAGIC     </div>
# MAGIC   </div>
# MAGIC </div>
# MAGIC
# MAGIC <!-- Card 2: Declarative -->
# MAGIC <div style="flex: 1; border: 2px solid #e0e0e0; border-radius: 12px; overflow: hidden; background: white;">
# MAGIC   <div style="background: #4299E0; color: white; padding: 14px 20px; text-align: center;">
# MAGIC     <div style="font-size: 18pt; font-weight: bold;">Declarative (This Lesson)</div>
# MAGIC   </div>
# MAGIC   <div style="padding: 18px 20px;">
# MAGIC     <div style="font-size: 14pt; color: #555; line-height: 1.6; margin-bottom: 14px;">
# MAGIC       You describe what each table should contain and where the data comes from. Databricks determines the execution order, handles incremental loading, and manages infrastructure automatically.
# MAGIC     </div>
# MAGIC     <div style="background: rgba(66,153,224,0.10); border-left: 4px solid #4299E0; padding: 10px 12px; border-radius: 6px; font-size: 14pt;">
# MAGIC       <strong>You say:</strong> "I want these tables with this data. You figure out how."
# MAGIC     </div>
# MAGIC   </div>
# MAGIC </div>
# MAGIC
# MAGIC </div>
# MAGIC
# MAGIC <!-- Key point callout -->
# MAGIC <div style="margin-top: 20px; padding: 16px 20px; background: #FFF6F4; border: 3px solid #FF5F46; border-radius: 10px;">
# MAGIC   <div style="font-size: 14pt; color: #0b2026; line-height: 1.6;">
# MAGIC     <strong>Same pipeline, less code, less orchestration.</strong> Spark Declarative Pipelines (SDP) handles execution order, incremental processing, error recovery, and infrastructure; you just define the tables.
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
# MAGIC **What Spark Declarative Pipelines handles for you**
# MAGIC
# MAGIC - **Execution order:** SDP reads your table definitions, figures out the dependencies (Bronze feeds Silver, Silver feeds Gold), and runs them in the right order. No task dependencies to configure.
# MAGIC - **Incremental processing:** Streaming tables automatically track which data has been processed. New files get picked up; old files are skipped. This is similar to COPY INTO but fully managed.
# MAGIC - **Infrastructure:** SDP provisions and manages the compute. You don't choose a cluster or configure serverless — it handles that.
# MAGIC - **Error handling:** If a step fails, SDP knows which downstream tables are affected and won't update them with stale data.
# MAGIC - **Data quality:** You can add expectations (quality rules) directly to your table definitions. SDP tracks violations and can warn or drop bad records.
# MAGIC
# MAGIC **Two key object types**
# MAGIC
# MAGIC - **Streaming tables** are for incremental ingestion. They process new data as it arrives and track what's already been loaded. Use these for your Bronze layer.
# MAGIC - **Materialized views** are for transformations. They recompute from their source each time the pipeline runs. Use these for Silver and Gold layers.
# MAGIC
# MAGIC </details>
# MAGIC
# MAGIC </div>

# COMMAND ----------

# MAGIC %md-sandbox
# MAGIC
# MAGIC <!-- LEARN: Three building blocks -->
# MAGIC <!-- Template: vertical-layered-stack (3 layers) -->
# MAGIC
# MAGIC <div style="max-width: 900px; margin: 0 auto; font-family: sans-serif;">
# MAGIC
# MAGIC <div style="font-size: 20pt; font-weight: 700; color: #0b2026; margin-bottom: 6px;">The Declarative Pipeline: Three Definitions, One Pipeline</div>
# MAGIC <div style="font-size: 14pt; color: #5A6F77; margin-bottom: 24px;">Each SQL cell below defines one layer of the Medallion Architecture. SDP reads all three and builds the full pipeline automatically.</div>
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
# MAGIC   <div style="font-size: 18pt; font-weight: 700;">Streaming Table — Bronze</div>
# MAGIC   <div style="font-size: 14pt; margin-top: 6px; opacity: 0.9;"><code style="background: rgba(255,255,255,0.2); padding: 2px 6px; border-radius: 4px;">CREATE OR REFRESH STREAMING TABLE</code> — ingests new files incrementally</div>
# MAGIC </div>
# MAGIC
# MAGIC <!-- Silver -->
# MAGIC <div style="background: #90A5B1; color: white; border-radius: 4px; padding: 18px 24px; text-align: center;">
# MAGIC   <div style="font-size: 16pt; font-weight: 700;">Materialized View — Silver</div>
# MAGIC   <div style="font-size: 14pt; margin-top: 6px; opacity: 0.9;"><code style="background: rgba(255,255,255,0.2); padding: 2px 6px; border-radius: 4px;">CREATE OR REFRESH MATERIALIZED VIEW</code> — transforms and validates with expectations</div>
# MAGIC </div>
# MAGIC
# MAGIC <!-- Gold -->
# MAGIC <div style="background: #FFAB00; color: #0b2026; border-radius: 4px 4px 8px 8px; padding: 18px 24px; text-align: center;">
# MAGIC   <div style="font-size: 16pt; font-weight: 700;">Materialized View — Gold</div>
# MAGIC   <div style="font-size: 14pt; margin-top: 6px; opacity: 0.85;"><code style="background: rgba(0,0,0,0.08); padding: 2px 6px; border-radius: 4px;">CREATE OR REFRESH MATERIALIZED VIEW</code> — aggregates for business consumption</div>
# MAGIC </div>
# MAGIC
# MAGIC </div>
# MAGIC
# MAGIC </div>
# MAGIC
# MAGIC </div>

# COMMAND ----------

# MAGIC %md
# MAGIC ---
# MAGIC ## Pipeline Definition: Bronze Layer
# MAGIC
# MAGIC The streaming table below reads all CSV files from the volume. The `STREAM` keyword tells SDP to track which files have been processed — just like COPY INTO, but fully managed.
# MAGIC
# MAGIC Compare this to Lesson 6 where you ran `CREATE TABLE` + `COPY INTO` as two separate steps.

# COMMAND ----------

# MAGIC %sql
CREATE OR REFRESH STREAMING TABLE current_employees_bronze_sdp
COMMENT "Raw employee data ingested from CSV files in the myfiles volume."
AS SELECT *
FROM STREAM read_files(
  '/Volumes/dbacademy/get_started_de/myfiles/',
  format => 'csv',
  header => true,
  inferSchema => true
);

# COMMAND ----------

# MAGIC %md
# MAGIC ---
# MAGIC ## Pipeline Definition: Silver Layer
# MAGIC
# MAGIC The materialized view below transforms Bronze into Silver, which are the same transformations done in Lesson 6 (uppercase Role, add timestamps), but with a bonus: **data quality expectations**.
# MAGIC
# MAGIC The `CONSTRAINT` lines define rules that SDP will track:
# MAGIC - `valid_id` — every row must have a non-null ID
# MAGIC - `valid_name` — every row must have a non-null FirstName

# COMMAND ----------

# MAGIC %sql
CREATE OR REFRESH MATERIALIZED VIEW current_employees_silver_sdp(
  CONSTRAINT valid_id EXPECT (ID IS NOT NULL),
  CONSTRAINT valid_name EXPECT (FirstName IS NOT NULL)
)
COMMENT "Cleaned and enriched employee data with data quality expectations."
AS SELECT
  ID,
  FirstName,
  Country,
  UPPER(Role) AS Role,
  current_timestamp() AS processed_timestamp,
  current_date() AS processed_date
FROM current_employees_bronze_sdp;

# COMMAND ----------

# MAGIC %md
# MAGIC ---
# MAGIC ## Pipeline Definition: Gold Layer
# MAGIC
# MAGIC The Gold materialized view aggregates Silver into a business-ready summary, same as the Gold layer in Lesson 6, but in a single declaration instead of a temp view + CREATE TABLE + INSERT OVERWRITE.

# COMMAND ----------

# MAGIC %sql
CREATE OR REFRESH MATERIALIZED VIEW total_roles_gold_sdp
COMMENT "Employee count by role — business-ready aggregation."
AS SELECT
  Role,
  COUNT(*) AS TotalEmployees
FROM current_employees_silver_sdp
GROUP BY Role;

# COMMAND ----------

# MAGIC %md
# MAGIC ---
# MAGIC ## That's the entire pipeline.
# MAGIC
# MAGIC Three SQL statements. No `CREATE TABLE` + `COPY INTO`. No task dependencies. No job configuration. SDP reads these three definitions, determines the order (Bronze → Silver → Gold), and runs them.
# MAGIC
# MAGIC Now let's set it up.

# COMMAND ----------

# MAGIC %md-sandbox
# MAGIC
# MAGIC <!-- LEARN: Comparison -->
# MAGIC
# MAGIC <div style="max-width: 900px; margin: 0 auto; font-family: sans-serif;">
# MAGIC
# MAGIC <div style="font-size: 20pt; font-weight: 700; color: #0b2026; margin-bottom: 16px;">Side-by-Side: Manual vs. Declarative</div>
# MAGIC
# MAGIC <table style="width: 100%; border-collapse: collapse; font-size: 14pt;">
# MAGIC   <tr style="background: #1B5162; color: white;">
# MAGIC     <th style="padding: 12px 16px; text-align: left; border-radius: 8px 0 0 0;">Step</th>
# MAGIC     <th style="padding: 12px 16px; text-align: left;">Imperative (Lessons 6-7)</th>
# MAGIC     <th style="padding: 12px 16px; text-align: left; border-radius: 0 8px 0 0;">Declarative (This Lesson)</th>
# MAGIC   </tr>
# MAGIC   <tr style="background: #F9F7F4;">
# MAGIC     <td style="padding: 10px 16px; font-weight: 600;">Bronze</td>
# MAGIC     <td style="padding: 10px 16px;">CREATE TABLE + COPY INTO (2 steps)</td>
# MAGIC     <td style="padding: 10px 16px;">CREATE OR REFRESH STREAMING TABLE (1 step)</td>
# MAGIC   </tr>
# MAGIC   <tr>
# MAGIC     <td style="padding: 10px 16px; font-weight: 600;">Silver</td>
# MAGIC     <td style="padding: 10px 16px;">CREATE OR REPLACE TABLE ... AS SELECT</td>
# MAGIC     <td style="padding: 10px 16px;">CREATE OR REFRESH MATERIALIZED VIEW + expectations</td>
# MAGIC   </tr>
# MAGIC   <tr style="background: #F9F7F4;">
# MAGIC     <td style="padding: 10px 16px; font-weight: 600;">Gold</td>
# MAGIC     <td style="padding: 10px 16px;">Temp view + CREATE TABLE + INSERT OVERWRITE (3 steps)</td>
# MAGIC     <td style="padding: 10px 16px;">CREATE OR REFRESH MATERIALIZED VIEW (1 step)</td>
# MAGIC   </tr>
# MAGIC   <tr>
# MAGIC     <td style="padding: 10px 16px; font-weight: 600;">Orchestration</td>
# MAGIC     <td style="padding: 10px 16px;">LakeFlow Job with 2 tasks + dependencies</td>
# MAGIC     <td style="padding: 10px 16px;">Automatic — SDP determines the order</td>
# MAGIC   </tr>
# MAGIC   <tr style="background: #F9F7F4;">
# MAGIC     <td style="padding: 10px 16px; font-weight: 600;">Data quality</td>
# MAGIC     <td style="padding: 10px 16px;">Not built in — you'd write checks manually</td>
# MAGIC     <td style="padding: 10px 16px;">CONSTRAINT expectations tracked automatically</td>
# MAGIC   </tr>
# MAGIC </table>
# MAGIC
# MAGIC </div>

# COMMAND ----------

# MAGIC %md
# MAGIC ---
# MAGIC ## Demo: Create and Run the Pipeline
# MAGIC
# MAGIC Now you'll configure an ETL Pipeline in the Databricks UI that uses this notebook as its source.
# MAGIC
# MAGIC **Follow these steps:**
# MAGIC
# MAGIC 1. In the left sidebar, click **Jobs & Pipelines** (right-click → open in a new tab so you can refer back to these instructions)
# MAGIC 2. Click **Create** and select **ETL Pipeline**
# MAGIC 3. Give your pipeline a name (e.g., `yourname-sdp-bronze-silver-gold`)
# MAGIC 4. Under **Source code**, click **Browse** and navigate to this notebook:
# MAGIC    - Find your project folder → select **08 - Build a Declarative Pipeline with Spark Declarative Pipelines**
# MAGIC 5. Under **Destination**, set:
# MAGIC    - **Catalog:** `dbacademy`
# MAGIC    - **Schema:** `get_started_de`
# MAGIC 6. Under **Compute**, confirm **Serverless** is selected
# MAGIC 7. Click **Create**

# COMMAND ----------

# MAGIC %md
# MAGIC ### Start the pipeline
# MAGIC
# MAGIC 1. Click **Start** in the top right of the pipeline editor
# MAGIC 2. Watch the pipeline graph appear. You should see three nodes: `current_employees_bronze_sdp` → `current_employees_silver_sdp` → `total_roles_gold_sdp`
# MAGIC 3. Each node will progress through: **Queued** → **Running** → **Completed**
# MAGIC 4. The pipeline typically takes 2-5 minutes to complete
# MAGIC
# MAGIC While it runs, notice how SDP automatically determined the execution order from your SQL definitions. You didn't configure any dependencies, it figured out that Silver reads from Bronze, and Gold reads from Silver.

# COMMAND ----------

# MAGIC %md
# MAGIC ### Explore the pipeline results
# MAGIC
# MAGIC Once the pipeline shows **Completed**:
# MAGIC
# MAGIC 1. **Click on `current_employees_silver_sdp`** in the pipeline graph
# MAGIC    - Look for the **Data Quality** section. You should see your two expectations (`valid_id` and `valid_name`) with pass/fail counts
# MAGIC 2. **Click on any node** and select **View in Catalog Explorer** to see the table details, lineage, and permissions
# MAGIC 3. Notice the **lineage** is automatically tracked. SDP knows exactly how each table was built
# MAGIC
# MAGIC When you're ready, head to the **Practice** notebook to query and compare the results.

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
# MAGIC       <li>Defined a full Bronze → Silver → Gold pipeline in <strong>3 SQL statements</strong></li>
# MAGIC       <li>Used a <strong>streaming table</strong> for incremental ingestion (Bronze)</li>
# MAGIC       <li>Used <strong>materialized views</strong> for transformations (Silver) and aggregations (Gold)</li>
# MAGIC       <li>Added <strong>data quality expectations</strong> to catch issues automatically</li>
# MAGIC       <li>Configured and ran an <strong>ETL Pipeline</strong> that handled orchestration, compute, and execution order for you</li>
# MAGIC     </ul>
# MAGIC     <div style="margin-top: 12px;">This is the same pipeline you built across Lessons 6 and 7, but declarative instead of imperative. In production, most Databricks data engineers use Spark Declarative Pipelines for exactly this reason: less code, automatic orchestration, and built-in data quality.</div>
# MAGIC   </div>
# MAGIC </div>
# MAGIC </div>

