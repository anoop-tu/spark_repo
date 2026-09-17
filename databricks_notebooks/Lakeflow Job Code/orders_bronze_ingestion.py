# Databricks notebook source
spark.sql("CREATE SCHEMA IF NOT EXISTS training_centralindia_lakeflowjobs_dbws.bronze_schema")

# COMMAND ----------

orders_csv_path = "abfss://dataset@lakeflowstorageaccount.dfs.core.windows.net/orders"

# COMMAND ----------

orders_df = (
spark.read.format("csv")
.option("header", True)
.option("inferSchema", True)
.load(orders_csv_path)
)

# COMMAND ----------

orders_df.write.format("delta").mode("overwrite").saveAsTable("training_centralindia_lakeflowjobs_dbws.bronze_schema.orders_bronze")

# COMMAND ----------

