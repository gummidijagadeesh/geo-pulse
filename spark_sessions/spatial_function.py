from pyspark.sql import SparkSession
import os
import sys

os.environ["PYSPARK_PYTHON"] = sys.executable
os.environ["PYSPARK_DRIVER_PYTHON"] = sys.executable


spark = SparkSession.builder.appName("GEO_PULSE").getOrCreate()


data = [
    ("dev_01", 17.28, 98.56),
    ("dev_02", 17.35, 98.16)
]

columns = ['device','lat','log']
df = spark.createDataFrame(data, schema=columns)
df.show()