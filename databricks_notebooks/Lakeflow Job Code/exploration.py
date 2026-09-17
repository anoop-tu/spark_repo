# Databricks notebook source
# MAGIC %sql
# MAGIC select * from ingest_schema.customers order by customerid;

# COMMAND ----------

# MAGIC %sql
# MAGIC select * from ingest_schema.customers where EffectiveEndDate is NULL;

# COMMAND ----------

# MAGIC %sql
# MAGIC select * from bronze_schema.customers_bronze

# COMMAND ----------

# MAGIC %sql
# MAGIC select count(*) from bronze_schema.orders_bronze;

# COMMAND ----------

