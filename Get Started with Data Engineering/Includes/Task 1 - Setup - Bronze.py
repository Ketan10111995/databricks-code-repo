# Databricks notebook source
# MAGIC %md
# MAGIC # Task 1: Setup and Bronze Layer
# MAGIC This notebook is used as a task in a LakeFlow Job. It sets up the catalog/schema and creates the Bronze table.

# COMMAND ----------

# Set catalog and schema
spark.sql("USE CATALOG dbacademy")
spark.sql("CREATE SCHEMA IF NOT EXISTS get_started_de")
spark.sql("USE SCHEMA get_started_de")

# Ensure volume and files exist
spark.sql("CREATE VOLUME IF NOT EXISTS myfiles")

volume_path = "/Volumes/dbacademy/get_started_de/myfiles"

try:
    files = [f.name for f in dbutils.fs.ls(volume_path)]
except:
    files = []

if "employees.csv" not in files:
    csv_data = """ID,FirstName,Country,Role
1,Kristi,United States,Data Engineer
2,Sophia,Germany,Data Analyst
3,Peter,Canada,ML Engineer
4,Zebi,India,Data Scientist"""
    dbutils.fs.put(f"{volume_path}/employees.csv", csv_data, overwrite=True)

if "employees2.csv" not in files:
    csv_data2 = """ID,FirstName,Country,Role
5,Maria,Brazil,Data Engineer
6,Aiden,Australia,Data Analyst"""
    dbutils.fs.put(f"{volume_path}/employees2.csv", csv_data2, overwrite=True)

print("Environment ready")

# COMMAND ----------

# Create Bronze table and load data
spark.sql("""
    CREATE TABLE IF NOT EXISTS current_employees_bronze_job (
        ID INT,
        FirstName STRING,
        Country STRING,
        Role STRING
    )
""")

result = spark.sql("""
    COPY INTO current_employees_bronze_job
    FROM '/Volumes/dbacademy/get_started_de/myfiles/'
    FILEFORMAT = CSV
    FORMAT_OPTIONS ('header' = 'true', 'inferSchema' = 'true')
""")
result.display()

print("Bronze table loaded")

# COMMAND ----------

# Verify
display(spark.sql("SELECT * FROM current_employees_bronze_job"))

