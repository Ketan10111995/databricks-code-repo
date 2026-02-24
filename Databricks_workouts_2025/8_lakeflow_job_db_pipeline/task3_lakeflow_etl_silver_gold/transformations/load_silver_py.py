from pyspark import pipelines as dp
from pyspark.sql.functions import *
@dp.table(name="catalog3_we47.schema3_we47.silver_shipments")
def load_silver():
    return spark.read.table("catalog3_we47.schema3_we47.bronze_shipments1").withColumn("loaddts", current_timestamp())