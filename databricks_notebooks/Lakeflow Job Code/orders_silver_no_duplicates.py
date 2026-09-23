# Databricks notebook source
spark.sql("CREATE SCHEMA IF NOT EXISTS training_centralindia_lakeflowjobs_dbws.silver_schema")

orders_cleaned = spark.table("training_centralindia_lakeflowjobs_dbws.silver_schema.orders_cleaned")

orders_cleaned.write.format("delta").mode("overwrite").saveAsTable("training_centralindia_lakeflowjobs_dbws.silver_schema.orders_dedupe")

# COMMAND ----------

