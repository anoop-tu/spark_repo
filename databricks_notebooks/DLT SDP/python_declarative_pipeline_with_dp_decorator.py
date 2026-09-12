from pyspark import pipelines as dp
from pyspark.sql.functions import current_timestamp, col, sum as _sum
from utilities import utils

source_path = spark.conf.get("source")

#Bronze ingest orders #orderid,orderdate,customerid,totalamount,status
@dp.table(name = "orders_bronze")
def orders_bronze():
    df = ( spark.readStream.format("cloudFiles")
           .option("cloudFiles.format", "csv")
           .option("cloudFiles.inferColumnTypes", "true")
           .load(f"{source_path}/orders")
           )
    return df.withColumn("ingesttime", current_timestamp()).withColumn("file_name", col("_metadata.file_path"))


#Bronze ingest cust  #customerid,customername,contactnumber,email,address,dateofbirth,registrationdate
@dp.table(name = "cust_bronze")
def cust_bronze():
    df = ( spark.readStream.format("cloudFiles")
           .option("cloudFiles.format", "csv")
           .option("cloudFiles.inferColumnTypes", "true")
           .load(f"{source_path}/customers")
           )
    return df.withColumn("ingesttime", current_timestamp()).withColumn("file_name", col("_metadata.file_path"))


#Silver orders
@dp.table(name = "orders_silver_cleaned")
@dp.expect_or_drop("valid_order","order_id is not null")
@dp.expect_or_drop("valid_cust","customer_id is not null")
def orders_silver_cleaned():
    return ( spark.readStream.table("orders_bronze")
            .withColumnRenamed("orderid", "order_id")
            .withColumnRenamed("orderdate", "order_date")
            .withColumnRenamed("customerid", "customer_id")
            .withColumnRenamed("totalamount", "total_amount")
            .withColumnRenamed("status", "status")
            .withColumnRenamed("file_name", "file_name")
            .withColumnRenamed("ingesttime", "ingesttime")
            .withColumn("amount_in_usd",utils.inr_to_usd(col("total_amount")))
    )


#Silver cust
@dp.table(name = "cust_silver_cleaned")
@dp.expect_or_drop("valid_cust","customer_id is not null")
def cust_silver_cleaned():
    return ( spark.readStream.table("cust_bronze")
            .withColumnRenamed("customerid", "customer_id")
            .withColumnRenamed("customername","customer_name")
            .withColumnRenamed("contactnumber","contact_number")
            .withColumnRenamed("dateofbirth","dob")
    )

# silver scd type 2 for customers, using Auto CDC

dp.create_streaming_table("customer_silver") # creates and empty target table. 

dp.create_auto_cdc_flow(
    target='customer_silver',
    source='cust_silver_cleaned',
    keys=['customer_id'],
    sequence_by="ingesttime",
    stored_as_scd_type=2 #Two hidden metadata columns get auto-added to the schema: __START_AT and __END_AT — using the same data type as your sequence_by column (ingesttime).
)


#silver scd type1 for customers, using Auto CDC
dp.create_streaming_table("orders_silver")
dp.create_auto_cdc_flow(
    target='orders_silver',
    source='orders_silver_cleaned',
    keys=['order_id'],
    sequence_by="ingesttime",
    stored_as_scd_type=1
)

#Gold city wise sales

@dp.materialized_view()
def city_wise_sales():
    current_customers = (
        spark.read.table("customer_silver")
        .filter(col("__END_AT").isNull())   # <-- FIX 2: keep only the CURRENT SCD2 version per customer
    )
    return (
        spark.read.table("orders_silver")
        .join(current_customers, "customer_id")
        .groupBy("address")
        .agg(_sum("amount_in_usd").alias("total_sales"))
        .withColumnRenamed("address", "city_name")
        .withColumnRenamed("total_sales", "total_sales_usd")
    )
    



