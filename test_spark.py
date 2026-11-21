from pyspark.sql import SparkSession

spark = (SparkSession.builder.appName("geo_pulse")
        .master("local[*]")
        .getOrCreate())


data = [
    ("dev_01", 17.3850, 78.4867),
    ("dev_02", 17.4000, 78.5000)
]

df = spark.createDataFrame(data, ['dev_id', 'lat', 'log'])

df.show()

spark.stop()