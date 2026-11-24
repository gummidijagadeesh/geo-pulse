from sedona.spark import SedonaContext

config = (
    SedonaContext.builder()
    .appName("GEO_PULSE_SEDONA")
    .master("local[2]")
    .config(
        "spark.jars.packages",
        "org.apache.sedona:sedona-spark-shaded-4.0_2.13:1.9.1"
    )
    .getOrCreate()
)

spark = SedonaContext.create(config)

print("Spark Version:", spark.version)

spark.sql("""
    SELECT ST_AsText(
        ST_Point(78.48, 17.38)
    ) AS geometry
""").show()

spark.stop()

