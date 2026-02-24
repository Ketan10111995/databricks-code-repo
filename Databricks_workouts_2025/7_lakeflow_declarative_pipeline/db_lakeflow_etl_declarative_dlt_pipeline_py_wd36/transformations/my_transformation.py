from pyspark import pipelines as dp
@dp.table()
def target_shipment_table():
    df1=spark.read.table("gcp_mysql_fc_wd36.logistics.shipments1")
    df2=df1.where("city is null")
    return df2