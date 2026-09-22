# Databricks notebook source
from pyspark.sql.functions import col

spark.sql("CREATE SCHEMA IF NOT EXISTS training_centralindia_lakeflowjobs_dbws.silver_schema")

# load cleaned customers from silver
customers_df = spark.table("silver_schema.customers_cleaned")

lookup_path = "abfss://dataset@lakeflowstorageaccount.dfs.core.windows.net/lookup"

city_state_df = spark.read.format("json").load(lookup_path)

customers_enriched = customers_df.join(
    city_state_df,
    customers_df.city == city_state_df.city,
    "left"
).drop(city_state_df.city) 

customers_enriched.write.format("delta").mode("overwrite").saveAsTable("silver_schema.customers_enriched")
