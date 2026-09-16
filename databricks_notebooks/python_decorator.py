# Databricks notebook source
# /// script
# [tool.databricks.environment]
# environment_version = "5"
# ///
def greet():
    print('hello!')

# COMMAND ----------

def my_decorator(func):
    def wrapper():
        print('Before func exec...')
        func()
        print('After func exec...')
    return wrapper

# COMMAND ----------

wrap = my_decorator(greet)
wrap()

# COMMAND ----------

@my_decorator
def greet():
    print('hello!')

# COMMAND ----------

greet()

# COMMAND ----------

def orders_bronzelatest():
    df = (
        spark.read
        .format('csv')
        .option('header','true')
        .option('inferSchema','true')
        .load('/Volumes/ext_cat/default/extvol/orders/orders1.csv')
    )
    return df

# COMMAND ----------

df = orders_bronzelatest()
df.show()

# COMMAND ----------

def write_to_delta(func):
    def wrapper():
        df = func()
        table_name = 'ext_cat.default.orders'
        df.write.format('delta').saveAsTable(table_name)
        print('Delta table created')
    return wrapper


# COMMAND ----------

@write_to_delta
def orders_bronzelatest():
    df = (
        spark.read
        .format('csv')
        .option('header','true')
        .option('inferSchema','true')
        .load('/Volumes/ext_cat/default/extvol/orders/orders1.csv')
    )
    return df


# COMMAND ----------

# MAGIC %sql
# MAGIC drop table ext_cat.default.orders

# COMMAND ----------

df = orders_bronzelatest()

# COMMAND ----------

# MAGIC %sql
# MAGIC select * from ext_cat.default.orders limit 10