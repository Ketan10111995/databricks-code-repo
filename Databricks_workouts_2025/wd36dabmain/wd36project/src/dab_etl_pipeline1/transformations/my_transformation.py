from pyspark import pipelines as dp
@dp.table()
def bronze_data_dab():
    df1=spark.createDataFrame([(1,'a','b','c'),(2,'d','e','f'),(3,'g','h','i'),(4,'j','k','l')])
    df2=df1.toDF('id','name1','name2','name3')
    return df2