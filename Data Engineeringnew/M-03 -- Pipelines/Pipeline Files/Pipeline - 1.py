# Pipeline source code

# Imports
# When using python, we import the pipelines and the functions modules
from pyspark import pipelines as dp
from pyspark.sql.functions import *

# Get pipeline configs
# We set these configs when we created the pipeline
# The code below captures these configs as python variables
catalog_name = spark.conf.get("catalog_name")
schema_name = spark.conf.get("schema_name")

# Define the source path using the configs
source_path = f'/Volumes/{catalog_name}/{schema_name}/myfiles/'

# Bronze table
# Read the CSV data from the source location using Auto Loader into a bronze-level table
@dp.table
def bronze_table():
    return (
        spark.readStream.format("cloudFiles") \
        .option("cloudFiles.format", "csv") \
        .option("header", "true") # Use this option if your CSV files have a header
        .load(source_path)
    )
    
# Silver-level table with some example transformation logic and data quality expectations
@dp.table
# The first expectation will warn us if the 'Country' column contains any values other than USA, India, and Pakistan
# The second expectation will drop any records where the 'Role' column is null or not one of the expected values
# The third expectation will fail the pipeline if the 'ID' column is null
@dp.expect("valid_country", "Country IN ('USA', 'India', 'Pakistan')")
@dp.expect_or_drop("valid_role", "Role IS NOT NULL AND Role IN ('INSTRUCTOR', 'MANAGER', 'DEVELOPER')")
@dp.expect_or_fail("valid_id", "ID IS NOT NULL")
def silver_table():
    return (
        spark.readStream.table("bronze_table") \
        .withColumn("id", col("id").cast("int")) \
        .withColumn("Role", upper(col("Role"))) \
        .select("ID", "Firstname", "Country", "Role")
    )

# Gold-level materialized view with an example aggregation
@dp.table
def gold_mv():
    return (
        spark.read.table("silver_table") \
        .groupBy("Role") \
        .agg(countDistinct("ID").alias("DistinctUsers"))
    )