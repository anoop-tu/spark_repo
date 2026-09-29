# # Consider a DF as below

# host_id, pat_id, claim_amount, claim_status, event_ts 
# H01, P01, 123, Rejected, D1
# H01, P02, 1213, Success, D1
# H01, P01, 1234, Rejected, D2
# H01, P03, 1213, Rejected, D1

# find the total and max claim amounts of a Hospital-Patient combination for each claim status, in a single row

# +------+-------+------------------+--------------------+----------------+------------------+-----------------+-------------------+
# |Pat-id|hosp-id|Approved_max_claim|Approved_total_claim|Denied_max_claim|Denied_total_claim|Pending_max_claim|Pending_total_claim|
# +------+-------+------------------+--------------------+----------------+------------------+-----------------+-------------------+
# |1     |H1     |500.0             |700.0               |150.0           |150.0             |0.0              |0.0                |
# |2     |H2     |0.0               |0.0                 |0.0             |0.0               |800.0            |800.0              |
# +------+-------+------------------+--------------------+----------------+------------------+-----------------+-------------------+


# Solution

# Option-1 - Using Pivot

from pyspark.sql import SparkSession
from pyspark.sql import functions as F

# 1. Initialize Spark (if not already done)
spark = SparkSession.builder.getOrCreate()

# Sample Data for demonstration
data = [
    (1, "H1", 500.0, "Approved", "2023-01-01"),
    (1, "H1", 200.0, "Approved", "2023-01-02"),
    (1, "H1", 150.0, "Denied",   "2023-01-03"),
    (2, "H2", 800.0, "Pending",  "2023-01-04")
]
columns = ["Pat-id", "hosp-id", "claim-amt", "claim-stat", "timestamp"]
df = spark.createDataFrame(data, columns)

# 2. Group, Pivot, and Aggregate
result_df = df.groupBy("Pat-id", "hosp-id") \
    .pivot("claim-stat") \
    .agg(
        F.max("claim-amt").alias("max_claim"),
        F.sum("claim-amt").alias("total_claim")
    )

# 3. (Optional) Replace nulls with 0 for statuses a patient didn't have
result_df = result_df.fillna(0)

result_df.show(truncate=False)


# Option-2 - Using 'when'

# from pyspark.sql import functions as F

# # Group by Patient and Hospital
result_df = df.groupBy("Pat-id", "hosp-id").agg(   
# --- APPROVED CLAIMS ---
    F.max(F.when(F.col("claim-stat") == "Approved", F.col("claim-amt"))).alias("Approved_max_claim"),
    F.sum(F.when(F.col("claim-stat") == "Approved", F.col("claim-amt"))).alias("Approved_total_claim"),    
# --- DENIED CLAIMS ---
    F.max(F.when(F.col("claim-stat") == "Denied", F.col("claim-amt"))).alias("Denied_max_claim"),
    F.sum(F.when(F.col("claim-stat") == "Denied", F.col("claim-amt"))).alias("Denied_total_claim"),    
    # --- PENDING CLAIMS ---
    F.max(F.when(F.col("claim-stat") == "Pending", F.col("claim-amt"))).alias("Pending_max_claim"),
    F.sum(F.when(F.col("claim-stat") == "Pending", F.col("claim-amt"))).alias("Pending_total_claim")    
   ).fillna(0) # Replace nulls with 0 for cleaner output

result_df.show(truncate=False)


# Q-2 - Suppose I have this data streaming from kafka and my watermark is 10 min. How not to lose the late arriving data

# Solution

# 1. The "Bronze Table" Pattern (Recommended)
# Do not read from Kafka directly into an aggregation. Instead, use the Medallion Architecture by writing the raw Kafka stream directly to a storage layer (like Delta Lake or Iceberg) first.

# Stream 1 (Ingest): Read from Kafka and write raw events to a Delta table. No watermarks, no aggregations. Every single record is saved, regardless of how late it is.

# Stream 2 (Aggregate): Read the stream from the Delta table, apply your 10-minute watermark, and perform your groupBy() and aggregations.

# Batch Reconciliation: Run a nightly batch job over the raw Delta table to recalculate the aggregations. This batch job will naturally include the late-arriving data that the real-time stream dropped, correcting your final dashboards.

# 2. Forking the Stream
# You can create two separate streaming queries from the same Kafka source dataframe.
kafka_df = spark.readStream.format("kafka")...

# Query 1: Save EVERYTHING to raw storage (No data loss)
raw_query = kafka_df.writeStream \
    .format("parquet") \
    .option("path", "/data/raw/") \
    .start()

# Query 2: Perform real-time aggregation (Drops data > 10 mins late)
agg_query = kafka_df \
    .withWatermark("timestamp", "10 minutes") \
    .groupBy(window("timestamp", "5 minutes"), "hosp-id") \
    .agg(...) \
    .writeStream \
    .format("console") \
    .start()
