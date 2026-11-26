import os
import sys
from pathlib import Path
from dotenv import load_dotenv
from pyspark.sql import SparkSession
from sedona.spark import SedonaContext



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