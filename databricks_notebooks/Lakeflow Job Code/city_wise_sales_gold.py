# Databricks notebook source
from pyspark.sql.functions import sum, current_timestamp, col

# step 1: ensure gold schema exists
spark.sql("CREATE SCHEMA IF NOT EXISTS training_centralindia_lakeflowjobs_dbws.gold_schema")

# step 2: load the silver tables
orders = spark.table("training_centralindia_lakeflowjobs_dbws.silver_schema.orders_dedupe")
customers = spark.table("training_centralindia_lakeflowjobs_dbws.silver_schema.customers_enriched")

# step 3: Join & aggregate by city
city_wise_sales = (
orders.join(customers, "customer_id")
.filter(col("city").isNotNull() & col("state").isNotNull())
.groupBy("state", "city")
.agg(sum("total_amount").alias("total_sales"))
)

# step 4: write it to the gold table
city_wise_sales.write.mode("overwrite").saveAsTable("training_centralindia_lakeflowjobs_dbws.gold_schema.city_wise_sales")

print("gold layer created")


