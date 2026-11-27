import os
import sys
from pathlib import Path
from dotenv import load_dotenv
from pyspark.sql import SparkSession
from sedona.spark import SedonaContext
from pyspark.sql.functions import expr



os.environ["PYSPARK_PYTHON"] = sys.executable
os.environ["PYSPARK_DRIVER_PYTHON"] = sys.executable


# Load .env from the project root
project_root = Path(__file__).resolve().parent.parent
load_dotenv(project_root / ".env")

sf_options = {
    "sfURL": os.environ["SNOWFLAKE_URL"],
    "sfUser": os.environ["SNOWFLAKE_USER"],
    "sfPassword": os.environ["SNOWFLAKE_PASSWORD"],
    "sfDatabase": "GEO_PULSE_DB",
    "sfSchema": "RAW_DATA",
    "sfWarehouse": os.environ["SNOWFLAKE_WAREHOUSE"]
}

packages = [
    "org.apache.sedona:sedona-spark-shaded-4.0_2.13:1.9.1",
    "net.snowflake:spark-snowflake_2.13:3.2.3-spark_4.0",
    "net.snowflake:snowflake-jdbc:4.0.2"
]

spark = (
    SedonaContext.builder()
    .appName("geo_pulse")
    .master("local[2]")
    .config("spark.jars.packages", ",".join(packages))
    .getOrCreate()
)

spark = SedonaContext.create(spark)


store = (
    spark.read
    .format("net.snowflake.spark.snowflake")
    .options(**sf_options)
    .option("dbtable", "STORE_DATA")
    .load()
)


store.show(5)


catchment_area = store.withColumn("catchment_area",
    expr("""
    st_buffer(st_transform(st_SetSRID(st_point(longitude,latitude),4326),
                'EPSG:32644'),500)"""))


catchment_area.show(5, truncate=False)

catchment_save = catchment_area.withColumn("catchment_wkt",
                expr("""st_AsText(catchment_area)"""))

catchment_save = catchment_save.drop("catchment_area")

catchment_save.printSchema()

"""catchment_save.write\
    .format("snowflake")\
    .options(**sf_options)\
    .option("dbtable","staging_data.store_catchment")\
    .mode("overwrite").save()"""

gps_ping = spark.read.format("net.snowflake.spark.snowflake")\
    .options(**sf_options)\
    .option("dbtable","gps_pings")\
    .load()

gps_ping.show()


#reading staging_table
store_catchment = spark.read\
                .format("net.snowflake.spark.snowflake")\
                .options(**sf_options)\
                .option("dbtable","staging_data.store_catchment")\
                .load()

store_catchment.show(5)


store_catchment.createOrReplaceTempView("store_catchment")
gps_ping.createOrReplaceTempView("gps_ping")


interact_data = spark.sql("""select 
                    s.store_id,
                    gp.ping_id,
                    gp.device_id,
                    gp.timestamp
                    from store_catchment s
                    inner join gps_ping gp
                    on st_Contains(st_GeomFromWKT(s.catchment_wkt),ST_GeomFromGeoJSON(gp.location))""")

interact_data.show(5, truncate=False)


spark.sql("""
    SELECT
        store_id,
        ST_AsText(ST_GeomFromWKT(catchment_wkt)) AS geometry
    FROM store_catchment
    LIMIT 2
""").show(truncate=False)

spark.sql("""
    SELECT
        ping_id,
        ST_AsText(ST_GeomFromGeoJSON(location)) AS geometry
    FROM gps_ping
    LIMIT 5
""").show(truncate=False)

print("Stores:", store_catchment.count())
print("GPS pings:", gps_ping.count())
