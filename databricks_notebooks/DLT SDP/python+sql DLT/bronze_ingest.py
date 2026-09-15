from pyspark import pipelines as dp
from pyspark.sql.functions import current_timestamp

# Programmatically generate a bronze table for each source system
sources = ["orders", "customers", "products"]

for source in sources:
    @dp.table(
        name=f"bronze_{source}",
        comment=f"Raw {source} data ingested via Auto Loader"
    )
    def _bronze_table(source=source):
        return (
            spark.readStream
            .format("cloudFiles")
            .option("cloudFiles.format", "json")
            .option("cloudFiles.schemaLocation", f"/schemas/{source}")
            .load(f"/mnt/raw/{source}/")
            .withColumn("_ingested_at", current_timestamp())
        )