# Databricks notebook source
from pyspark.sql.functions import col

spark.sql("CREATE SCHEMA IF NOT EXISTS training_centralindia_lakeflowjobs_dbws.silver_schema")

customers_cleaned = (spark.table("training_centralindia_lakeflowjobs_dbws.bronze_schema.customers_bronze")
.filter(col("EffectiveEndDate").isNull()) # keep only current records
.select(
  col("CustomerID").alias("customer_id"),
  col("CustomerName").alias("customer_name"),
  col("ContactNumber").alias("contact_number"),
  col("Email").alias("email"),
  col("Address").alias("city"),
  col("DateOfBirth").alias("dob"),
  col("RegistrationDate").alias("registration_date")
  ))

# COMMAND ----------

customers_cleaned.write.mode("overwrite").saveAsTable("training_centralindia_lakeflowjobs_dbws.silver_schema.customers_cleaned")

print("customers cleaned complete: silver_schema.customers_cleaned")

# COMMAND ----------

# MAGIC %sql
# MAGIC drop table training_centralindia_lakeflowjobs_dbws.silver_schema.customers_cleaned;

# COMMAND ----------

# MAGIC %sql
# MAGIC create schema if not exists training_centralindia_lakeflowjobs_dbws.silver_schema;
# MAGIC
# MAGIC create or replace table training_centralindia_lakeflowjobs_dbws.silver_schema.customers_cleaned 
# MAGIC using DELTA
# MAGIC AS 
# MAGIC SELECT 
# MAGIC   CustomerID as customer_id,
# MAGIC   CustomerName as customer_name,
# MAGIC   ContactNumber as contact_number,
# MAGIC   Email as email,
# MAGIC   Address as city,
# MAGIC   DateOfBirth as  dob,
# MAGIC   RegistrationDate as registration_date
# MAGIC FROM training_centralindia_lakeflowjobs_dbws.bronze_schema.customers_bronze
# MAGIC WHERE EffectiveEndDate is null;

# COMMAND ----------

