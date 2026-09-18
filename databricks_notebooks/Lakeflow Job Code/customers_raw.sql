-- CREATE SCHEMA
CREATE SCHEMA IF NOT EXISTS ingest_schema;

-- CREATE TABLE
CREATE TABLE IF NOT EXISTS ingest_schema.customers(
    CustomerID INT,
    CustomerName STRING,
    ContactNumber STRING, 
    Email STRING,
    Address STRING,
    DateOfBirth DATE,
    RegistrationDate DATE,
    EffectiveStartDate TIMESTAMP,
    EffectiveEndDate TIMESTAMP
) USING DELTA
TBLPROPERTIES ('delta.enableChangeDataFeed' = 'true');

-- CURRENT VERSIONS (your original data; EffectiveEndDate = NULL)
INSERT INTO ingest_schema.customers VALUES
('1','Tara Yadav','9682667034','diya.desai@hotmail.com','Bhopal','1980-01-01','2020-01-01', current_timestamp(), NULL),
('2','Vivaan Joshi','9367873685','nikhil.patel@gmail.com','Visakhapatnam','1980-01-08','2020-01-04', current_timestamp(), NULL),
('3','Tara Bhatt','9537576916','ananya.patel@hotmail.com','Chennai','1980-01-15','2020-01-07', current_timestamp(), NULL),
('4','Vihaan Nair','9438442737','meera.singh@hotmail.com','Thane','1980-01-22','2020-01-10', current_timestamp(), NULL),
('5','Saanvi Gupta','9160494581','vivaan.agarwal@outlook.com','Vadodara','1980-01-29','2020-01-13', current_timestamp(), NULL),
('6','Aarav Bhatt','9534050225','diya.agarwal@gmail.com','Patna','1980-02-05','2020-01-16', current_timestamp(), NULL),
('7','Rohan Patel','9781548245','aryan.joshi@hotmail.com','Indore','1980-02-12','2020-01-19', current_timestamp(), NULL),
('8','Meera Jain','9215158173','aryan.rao@outlook.com','Delhi','1980-02-19','2020-01-22', current_timestamp(), NULL),
('9','Saanvi Gupta','9720248136','rohan.bhatt@yahoo.com','Ludhiana','1980-02-26','2020-01-25', current_timestamp(), NULL),
('10','Vihaan Agarwal','9668523834','saanvi.sharma@outlook.com','Lucknow','1980-03-04','2020-01-28', current_timestamp(), NULL),
('11','Rohan Yadav','9969140009','ishaan.singh@gmail.com','Kanpur','1980-03-11','2020-01-31', current_timestamp(), NULL),
('12','Aarav Joshi','9581733251','kavya.reddy@yahoo.com','Lucknow','1980-03-18','2020-02-03', current_timestamp(), NULL),
('13','Meera Bhatt','9389797496','vihaan.jain@gmail.com','Mumbai','1980-03-25','2020-02-06', current_timestamp(), NULL),
('14','Manan Iyer','9270284531','krish.patel@yahoo.com','Bhopal','1980-04-01','2020-02-09', current_timestamp(), NULL),
('15','Advika Gupta','9394139940','manan.choudhury@hotmail.com','Pune','1980-04-08','2020-02-12', current_timestamp(), NULL),
('16','Vihaan Verma','9299923279','vivaan.bhatt@hotmail.com','Bengaluru','1980-04-15','2020-02-15', current_timestamp(), NULL),
('17','Tara Bhatt','9498213461','kavya.verma@yahoo.com','Delhi','1980-04-22','2020-02-18', current_timestamp(), NULL),
('18','Diya Agarwal','9109402581','nikhil.shah@gmail.com','Indore','1980-04-29','2020-02-21', current_timestamp(), NULL),
('19','Prisha Bhat','9678462978','nikhil.yadav@gmail.com','Ghaziabad','1980-05-06','2020-02-24', current_timestamp(), NULL),
('20','Krish Sharma','9626702643','kavya.bhat@hotmail.com','Bengaluru','1980-05-13','2020-02-27', current_timestamp(), NULL),
('21','Tara Verma','9859917249','tara.jain@yahoo.com','Vadodara','1980-05-20','2020-03-01', current_timestamp(), NULL),
('22','Kabir Rao','9894536295','vihaan.shah@yahoo.com','Patna','1980-05-27','2020-03-04', current_timestamp(), NULL),
('23','Vihaan Nair','9864467575','aarav.iyer@outlook.com','Ahmedabad','1980-06-03','2020-03-07', current_timestamp(), NULL),
('24','Rohan Yadav','9870465008','rohan.choudhury@hotmail.com','Jaipur','1980-06-10','2020-03-10', current_timestamp(), NULL),
('25','Arjun Joshi','9275730158','advika.jain@outlook.com','Bengaluru','1980-06-17','2020-03-13', current_timestamp(), NULL),
('26','Nikhil Reddy','9629593712','diya.desai@yahoo.com','Vadodara','1980-06-24','2020-03-16', current_timestamp(), NULL),
('27','Diya Desai','9717610700','aarav.joshi@hotmail.com','Thane','1980-07-01','2020-03-19', current_timestamp(), NULL),
('28','Rohan Joshi','9103108033','meera.shah@outlook.com','Delhi','1980-07-08','2020-03-22', current_timestamp(), NULL),
('29','Arjun Yadav','9444790238','kabir.patel@gmail.com','Lucknow','1980-07-15','2020-03-25', current_timestamp(), NULL),
('30','Arjun Gupta','9247812034','kavya.mehta@hotmail.com','Bhopal','1980-07-22','2020-03-28', current_timestamp(), NULL),
('31','Prisha Agarwal','9458140537','ananya.joshi@gmail.com','Hyderabad','1980-07-29','2020-03-31', current_timestamp(), NULL),
('32','Ananya Patel','9181941035','kabir.choudhury@outlook.com','Mumbai','1980-08-05','2020-04-03', current_timestamp(), NULL),
('33','Vivaan Singh','9511942388','saanvi.patel@hotmail.com','Patna','1980-08-12','2020-04-06', current_timestamp(), NULL),
('34','Aarav Reddy','9522930495','meera.reddy@gmail.com','Visakhapatnam','1980-08-19','2020-04-09', current_timestamp(), NULL),
('35','Riya Jain','9428804190','aryan.yadav@outlook.com','Vadodara','1980-08-26','2020-04-12', current_timestamp(), NULL),
('36','Manan Desai','9888979277','nikhil.bhatt@hotmail.com','Pune','1980-09-02','2020-04-15', current_timestamp(), NULL),
('37','Ananya Shah','9436566647','manan.agarwal@yahoo.com','Ludhiana','1980-09-09','2020-04-18', current_timestamp(), NULL),
('38','Kabir Reddy','9584705224','aarav.bhat@yahoo.com','Delhi','1980-09-16','2020-04-21', current_timestamp(), NULL),
('39','Nikhil Singh','9504675679','aryan.joshi@yahoo.com','Mumbai','1980-09-23','2020-04-24', current_timestamp(), NULL),
('40','Kavya Gupta','9463516169','krish.singh@yahoo.com','Chennai','1980-09-30','2020-04-27', current_timestamp(), NULL)
;

-- HISTORICAL VERSIONS (SCD2) FOR A FEW CUSTOMERS
-- These represent the prior state and are end-dated just before now.

-- Customer 1: previously lived in Indore, different email
INSERT INTO ingest_schema.customers VALUES
('1','Tara Yadav','9682667034','tara.yadav@gmail.com','Indore',
 '1980-01-01','2020-01-01',
 current_timestamp() - INTERVAL 30 DAYS,
 current_timestamp() - INTERVAL 1 SECOND);

-- Customer 5: older phone and city
INSERT INTO ingest_schema.customers VALUES
('5','Saanvi Gupta','9160490000','vivaan.agarwal@outlook.com','Surat',
 '1980-01-29','2020-01-13',
 current_timestamp() - INTERVAL 45 DAYS,
 current_timestamp() - INTERVAL 1 SECOND);

-- Customer 7: older email
INSERT INTO ingest_schema.customers VALUES
('7','Rohan Patel','9781548245','rohan.patel@yahoo.com','Indore',
 '1980-02-12','2020-01-19',
 current_timestamp() - INTERVAL 60 DAYS,
 current_timestamp() - INTERVAL 1 SECOND);

-- Customer 10: previously in Delhi
INSERT INTO ingest_schema.customers VALUES
('10','Vihaan Agarwal','9668523834','saanvi.sharma@outlook.com','Delhi',
 '1980-03-04','2020-01-28',
 current_timestamp() - INTERVAL 90 DAYS,
 current_timestamp() - INTERVAL 1 SECOND);










