# Databricks notebook source
from pyspark.sql.functions import col, to_date, row_number
from pyspark.sql.window import Window

# Step 1: Ensure silver schema exists in default catalog
spark.sql("CREATE SCHEMA IF NOT EXISTS training_centralindia_lakeflowjobs_dbws.silver_schema")

# Step 2: Load Bronze orders
bronze_orders = spark.table("training_centralindia_lakeflowjobs_dbws.bronze_schema.orders_bronze")

# Step 3: Rename and cast columns
orders_cleaned = (
    bronze_orders
    .select(
        col("OrderID").alias("order_id"),
        to_date(col("OrderDate")).alias("order_date"),
        col("CustomerID").alias("customer_id"),
        col("TotalAmount").cast("double").alias("total_amount"),
        col("Status").alias("status")
    )
)

# Step 4: Write to Silver layer
orders_cleaned.write.format("delta").mode("overwrite").saveAsTable("training_centralindia_lakeflowjobs_dbws.silver_schema.orders_cleaned")
print("✅ Silver cleaned complete: training_centralindia_lakeflowjobs_dbws.silver_schema.orders_cleaned")



# COMMAND ----------

orders_cleaned.show(500)

# COMMAND ----------

w = Window.partitionBy("order_id").orderBy(col("order_date").desc())

order_with_rn = orders_cleaned.withColumn("rn", row_number().over(w))

# COMMAND ----------

order_with_rn.show(500)

# COMMAND ----------

total_cleaned = orders_cleaned.count()
total_dedupe = order_with_rn.filter(col("rn") == 1).count()

duplicate_exists = total_cleaned != total_dedupe


# COMMAND ----------

dbutils.jobs.taskValues.set(key="has_duplicates", value=duplicate_exists)

# COMMAND ----------

