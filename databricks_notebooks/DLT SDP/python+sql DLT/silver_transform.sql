CREATE OR REFRESH STREAMING TABLE silver_orders
(
  CONSTRAINT valid_order_id EXPECT (order_id IS NOT NULL) ON VIOLATION DROP ROW,
  CONSTRAINT valid_amount EXPECT (amount > 0) ON VIOLATION DROP ROW
)
COMMENT "Cleaned orders with basic quality checks"
AS SELECT
  order_id,
  customer_id,
  amount,
  order_date,
  _ingested_at
FROM STREAM bronze_orders;

CREATE OR REFRESH MATERIALIZED VIEW silver_customers
AS SELECT
  customer_id,
  UPPER(TRIM(name)) AS name,
  email,
  region
FROM bronze_customers
WHERE customer_id IS NOT NULL;