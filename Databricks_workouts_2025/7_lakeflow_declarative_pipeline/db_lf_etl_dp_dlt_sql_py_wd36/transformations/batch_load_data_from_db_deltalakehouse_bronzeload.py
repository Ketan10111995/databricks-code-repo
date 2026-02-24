from pyspark import pipelines

#load_data_bronze_imp_dp().write.saveAsTable("lakehousecat.default.shipment1_bronze")
@pipelines.table(name="catalog1_we47.schema1_we47.shipment1_bronze1")#it becomes declarative by specifying decorator on top of the function
def load_data_bronze_imp_dp():#Imperative program
    df1=spark.read.table("gcp_mysql_fc_wd36.logistics.shipments1")#foreign catalog external DB source
    df2=df1.filter("city is null")
    return df2