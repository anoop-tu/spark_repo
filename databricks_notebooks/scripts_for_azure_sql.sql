create table dbo.orders(
order_id INT PRIMARY KEY,
order_date DATETIME,
customer_id int,
order_status VARCHAR(50)
);
---------------------------------------------
create TABLE dbo.customers(
customer_id int PRIMARY KEY,
first_name VARCHAR(50),
last_name VARCHAR(50),
phone VARCHAR(20),
email VARCHAR(50),
address VARCHAR(200),
city VARCHAR(50),
state VARCHAR(50),
zip VARCHAR(10)
);
---------------------------------------------
-- enable either CDC otr CT for tracking the changes
alter DATABASE [managed-connector-demo-db]
set CHANGE_TRACKING = ON
(CHANGE_RETENTION = 3 DAYS, AUTO_CLEANUP = ON);
---------------------------------------------
alter table dbo.orders
ENABLE CHANGE_TRACKING
with (TRACK_COLUMNS_UPDATED = ON);
---------------------------------------------
alter table dbo.customers
ENABLE CHANGE_TRACKING
with (TRACK_COLUMNS_UPDATED = ON);

---------------------------------------------

--execute script - https://learn.microsoft.com/en-us/azure/databricks/_extras/documents/ddl_support_objects.sql  
-- to enable CDC for DDL statments, that add/remove columns etc on the tables.

---Note:
---In the DDL script, make sure you apply the following changes before running it in the Azure SQL Query Editor:
---
----- Set the mode to Change Tracking (CT)
---DECLARE @mode NVARCHAR(10);
---SET @mode = 'CT';   -- ['BOTH' | 'CT' | 'CDC' | 'NONE']
---
----- Set your username/schema owner (for example: dbo)
---DECLARE @replicationUser NVARCHAR(100);
---SET @replicationUser = 'dbo';  -- Replace with your actual username if different
---
---This ensures that:
---•    The ingestion is configured for Change Tracking (CT) mode.
---•    The replication user context is set correctly (usually dbo for Azure SQL).

---------------------------------------------
INSERT INTO dbo.customers
(customer_id, first_name, last_name, phone, email, address, city, state, zip)
VALUES
(101, 'Amit', 'Sharma', '9876543210', 'amit.sharma@email.com', '12 MG Road', 'Bengaluru', 'Karnataka', '560001'),
(102, 'Priya', 'Nair', '9876543211', 'priya.nair@email.com', '45 Kowdiar Road', 'Thiruvananthapuram', 'Kerala', '695003'),
(103, 'Rahul', 'Verma', '9876543212', 'rahul.verma@email.com', '78 Park Street', 'Kolkata', 'West Bengal', '700016'),
(104, 'Sneha', 'Iyer', '9876543213', 'sneha.iyer@email.com', '23 Anna Nagar', 'Chennai', 'Tamil Nadu', '600040'),
(105, 'Arjun', 'Mehta', '9876543214', 'arjun.mehta@email.com', '56 Satellite Road', 'Ahmedabad', 'Gujarat', '380015'),
(106, 'Neha', 'Kapoor', '9876543215', 'neha.kapoor@email.com', '89 Sector 17', 'Chandigarh', 'Chandigarh', '160017'),
(107, 'Vikram', 'Reddy', '9876543216', 'vikram.reddy@email.com', '34 Banjara Hills', 'Hyderabad', 'Telangana', '500034'),
(108, 'Anjali', 'Patel', '9876543217', 'anjali.patel@email.com', '67 FC Road', 'Pune', 'Maharashtra', '411004'),
(109, 'Karan', 'Singh', '9876543218', 'karan.singh@email.com', '90 Civil Lines', 'Jaipur', 'Rajasthan', '302006'),
(110, 'Meera', 'Thomas', '9876543219', 'meera.thomas@email.com', '15 Marine Drive', 'Kochi', 'Kerala', '682011');

INSERT INTO dbo.orders
(order_id, order_date, customer_id, order_status)
VALUES
(10001, '2026-08-01 10:15:00', 101, 'Delivered'),
(10002, '2026-08-03 14:30:00', 102, 'Shipped'),
(10003, '2026-08-05 09:45:00', 103, 'Delivered'),
(10004, '2026-08-07 16:20:00', 104, 'Processing'),
(10005, '2026-08-10 11:10:00', 105, 'Delivered'),
(10006, '2026-08-12 13:50:00', 101, 'Delivered'),
(10007, '2026-08-15 18:05:00', 106, 'Cancelled'),
(10008, '2026-08-18 10:40:00', 107, 'Shipped'),
(10009, '2026-08-20 15:25:00', 104, 'Processing'),
(10010, '2026-08-22 12:00:00', 108, 'Delivered');
---------------------------------------------
