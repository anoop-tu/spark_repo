

# 1. Function Returning a Transformed DataFrame
from pyspark.sql import DataFrame
import pyspark.sql.functions as F


# 1. Function Returning a Transformed DataFrame
# This approach couples the transformation logic directly to the DataFrame schema and structure.

def clean_phone_numbers(df: DataFrame, input_col: str, output_col: str) -> DataFrame:
    """Transforms a DataFrame by cleaning phone number digits."""
    return df.withColumn(
        output_col,
        F.regexp_replace(F.col(input_col), r"[^0-9]", "")
    )

# Usage:
# Direct DataFrame-to-DataFrame transformation
cleaned_df = clean_phone_numbers(customer_df, input_col="phone", output_col="phone_clean")

# Stop writing PySpark functions that take a full DataFrame just to transform a single column.
# Coupling single-column mappings to an entire DataFrame locks your logic into specific schemas and makes unit testing unnecessarily heavy.

#2. Function Returning a Column Expression (Preferred for Mappings)
from pyspark.sql import Column
import pyspark.sql.functions as F

def clean_phone_col(col: Column | str) -> Column:
    """Returns a Column expression that strips non-digit characters."""
    col = F.col(col) if isinstance(col, str) else col
    return F.regexp_replace(col, r"[^0-9]", "")

# Usage 1: Inside .withColumn()
df_with_clean_phone = customer_df.withColumn("phone_clean", clean_phone_col("phone"))

# Usage 2: Inside .select() across multiple columns simultaneously
multi_cleaned_df = customer_df.select(
    "id",
    clean_phone_col("home_phone").alias("home_phone_clean"),
    clean_phone_col("mobile_phone").alias("mobile_phone_clean")
)

# Usage 3: Composing inside another Column expression (e.g., conditional logic)
flagged_df = customer_df.withColumn(
    "is_valid_len",
    F.length(clean_phone_col("phone")) == 10
)

# By normalizing col: Column | str, you unlock two flexible calling patterns:
# Pass the column name directly. The function wraps it with F.col() under the hood:

df.withColumn("phone_clean", clean_phone_col("phone"))

# Pass existing Column references or nested transformations without redundant wrapping:
# Multiple columns in a single select
df.select(
    clean_phone_col(F.col("home_phone")).alias("home_phone_clean"),
    clean_phone_col(F.col("mobile_phone")).alias("mobile_phone_clean")
)

# Chained inside another transformation
df.withColumn("is_valid", F.length(clean_phone_col(F.trim("phone"))) == 10)


# Why this pattern wins:
# True Composability: Nest it inside .select(), .withColumn(), or F.when().

# Catalyst Friendly: Remains lazily evaluated within Spark's logical plan.

# Trivial Unit Testing: Test logic at the column expression level without spinning up dummy DataFrames.