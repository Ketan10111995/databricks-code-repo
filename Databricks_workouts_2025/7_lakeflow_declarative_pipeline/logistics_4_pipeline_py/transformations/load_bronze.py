from pyspark import pipelines as dp

@dp.table(name="bronze_staff_data1")
def bronze_staff_data():

    return (spark.readStream
            .format("cloudFiles")
            .option("cloudFiles.format", "csv")
            .option("inferColumnTypes", "true")
            .option("cloudFiles.schemaEvolutionMode","addNewColumns")
            .load("/Volumes/catalog/schema/datalake/staff/_delta_log/"))


@dp.table(name="bronze_geotag_data1")
def bronze_geotag_data():

    return (
        spark.readStream
            .format("cloudFiles")
            .option("cloudFiles.format", "csv")
            .option("inferColumnTypes", "true")
            .load("/Volumes/catalog/schema/silver/geotag")
    )


@dp.table(name="bronze_shipments_data1")
def bronze_shipments_data():

    return (
        spark.readStream
            .format("cloudFiles")
            .option("cloudFiles.format", "json")
            .option("inferColumnTypes", "true")
            .option("multiLine", "true")
            .load("/Volumes/catalog/schema/silver/shipments/")
            .select(
                "shipment_id",
                "order_id",
                "source_city",
                "destination_city",
                "shipment_status",
                "cargo_type",
                "vehicle_type",
                "payment_mode",
                "shipment_weight_kg",
                "shipment_cost",
                "shipment_date"
            )
    )