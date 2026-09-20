# Databricks notebook source
from pyspark.sql.functions import col, sum, current_timestamp

state_param = dbutils.widgets.get("state")

print(f"Processing state: {state_param}")

gold_df = spark.table("gold_schema.city_wise_sales")

# filter for current state
state_df = gold_df.filter(col("state") == state_param)

state_final_df = state_df.withColumn("large_city",
                    (col("total_sales") > 10000).cast("boolean")
)

state_final_df.write.format("delta").option("mergeSchema", "true").mode("overwrite").saveAsTable(f"gold_schema.state_sales_{state_param.lower()}")
