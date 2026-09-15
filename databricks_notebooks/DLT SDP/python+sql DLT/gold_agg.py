from pyspark import pipelines as dp
from pyspark.sql.functions import col, udf
from pyspark.sql.types import StringType

# Reusable business logic — unit-testable outside the pipeline too
def classify_spend(amount: float) -> str:
    if amount is None:
        return "unknown"
    elif amount < 50:
        return "low"
    elif amount < 500:
        return "medium"
    return "high"

classify_spend_udf = udf(classify_spend, StringType())

@dp.table(
    name="gold_customer_spend",
    comment="Customer-level spend summary with tiering"
)
def gold_customer_spend():
    orders = dp.read("silver_orders")
    customers = dp.read("silver_customers")

    return (
        orders.join(customers, "customer_id")
        .groupBy("customer_id", "name", "region")
        .sum("amount")
        .withColumnRenamed("sum(amount)", "total_spend")
        .withColumn("spend_tier", classify_spend_udf(col("total_spend")))
    )