from pyspark import pipelines as dp

@dp.table(name="catalog1_we47.schema1_we47.drugs_stream_bronze_table")
def streaming_load():
  df1=spark.readStream.table("lakehousecat1.deltadb.drugstbl")
  return df1