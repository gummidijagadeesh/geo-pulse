from pyspark.sql import SparkSession

spark = SparkSession.builder.appName("geo").getOrCreate()

spark.range(5).show()