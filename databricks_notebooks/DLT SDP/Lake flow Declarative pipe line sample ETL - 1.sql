create streaming table ext_cat.default.orders_bronze
as
select * ,
_metadata.file_path as filename,
current_timestamp() as ingestion_ts
from 
cloud_files(
    '/Volumes/ext_cat/default/extvol/orders/' ,'csv',map('cloudFiles.inferColumnTypes','true')
);

create streaming table ext_cat.default.customers_bronze
as
select * ,
_metadata.file_path as filename,
current_timestamp() as ingestion_ts
from 
cloud_files(
    '/Volumes/ext_cat/default/extvol/customers/' ,'csv',map('cloudFiles.inferColumnTypes','true')
);

create streaming table ext_cat.default.orders_silver_cleaned (
    constraint valid_orders expect (order_id is not null) on violation drop row,
    constraint valid_cust expect (customer_id is not null) on violation drop row
)
as
select orderid as order_id,
orderdate as order_date,
customerid as customer_id,
totalamount as total_amount,
status,
filename as file_name,
ingestion_ts
from 
STREAM(live.orders_bronze);


create streaming table ext_cat.default.customers_silver_cleaned (
    constraint valid_orders expect (customer_id is not null) on violation drop row
)
as
select customerid as customer_id,
customername as customer_name,
address as city,
dateofbirth as dob,
registrationdate as customer_since,
filename as file_name,
ingestion_ts
from 
STREAM(live.customers_bronze);

create streaming table ext_cat.default.customers_silver;
Apply changes into live.customers_silver from STREAM(live.customers_silver_cleaned)
keys(customer_id)
sequence by ingestion_ts
stored as scd type 2;

create streaming table ext_cat.default.orders_silver;
-- Apply changes into live.orders_silver from STREAM(live.orders_silver_cleaned)
-- keys(order_id)
-- sequence by ingestion_ts;
create flow orders_silver_flow as 
auto cdc into orders_silver
from STREAM(live.orders_silver_cleaned)
keys(order_id)
sequence by ingestion_ts;


create materialized view city_wise_sales_gold
as
select city,sum(total_amount) as total_sales
from live.orders_silver o
join live.customers_silver c
on o.customer_id = c.customer_id
group by city;