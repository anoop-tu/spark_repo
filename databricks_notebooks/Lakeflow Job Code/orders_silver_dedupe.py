# Databricks notebook source
from pyspark.sql.functions import col, to_date, row_number
from pyspark.sql.window import Window

spark.sql("CREATE SCHEMA IF NOT EXISTS training_centralindia_lakeflowjobs_dbws.silver_schema")

orders_cleaned = spark.table("training_centralindia_lakeflowjobs_dbws.silver_schema.orders_cleaned")




# COMMAND ----------

w = Window.partitionBy("order_id").orderBy(col("order_date").desc())

order_with_rn = orders_cleaned.withColumn("rn", row_number().over(w))



# COMMAND ----------

orders_dedupe = order_with_rn.filter(col("rn") == 1).drop("rn")


# COMMAND ----------

orders_dedupe.write.format("delta").mode("overwrite").saveAsTable("training_centralindia_lakeflowjobs_dbws.silver_schema.orders_dedupe")

# COMMAND ----------

