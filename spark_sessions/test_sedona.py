from pyspark.sql import SparkSession
from sedona.spark import SedonaContext

config = SedonaContext.builder.appName('GEO_PULSE_SEDONA').getOrCreate()


spark = SedonaContext.create(config)

print(spark.version)


spark.sql(
    """
    SELECT ST_AsText(
        ST_Point(78.48, 17.38)
    ) AS geometry"""
).show()

