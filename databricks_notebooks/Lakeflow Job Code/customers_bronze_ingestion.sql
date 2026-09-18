
-- STEP 1: Ensure Bronze Schema Exists
CREATE SCHEMA IF NOT EXISTS bronze_schema;

-- STEP 2: 
CREATE OR REPLACE TABLE bronze_schema.customers_bronze AS
SELECT 
  CustomerID,
  CustomerName,
  ContactNumber,
  Email,
  Address,
  DateOfBirth,
  RegistrationDate,
  EffectiveStartDate,
  EffectiveEndDate
FROM ingest_schema.customers;
  
