from pyspark.sql import SparkSession

spark = SparkSession. \
builder. \
appName("week9-assignment-2"). \
config("spark.sql.warehouse.dir", "/user/itv027484/warehouse"). \
enableHiveSupport(). \
master('yarn'). \
getOrCreate()

from pyspark.sql.types import *
from pyspark.sql.functions import *

user_address_schema = StructType([
    StructField("city",StringType()),
    StructField("street",StringType()),
    StructField("state",StringType()),
    StructField("postal_code",StringType()),
])
user_schema = StructType ([
    StructField("user_id",LongType()),
    StructField("user_first_name",StringType()),
    StructField("user_last_name",StringType()),
    StructField("user_email",StringType()),
    StructField("user_gender",StringType()),
    StructField("user_phone_numbers",ArrayType(StringType())),
    StructField("user_address",user_address_schema)    
])


df1 = spark.read.format('json').schema(user_schema).load('/public/sms/users')

print('------------------------------------')
print('Count of records in file')
print(df1.count())

print('------------------------------------')
print('Count of users from the state New York')
print(df1.where(df1.user_address.state == "New York").count())

print('------------------------------------')
print('State which has maximum number of postal codes')
df1.select(df1.user_address.state.alias("state") , df1.user_address.postal_code.alias("postal_code")) \
.groupBy("state").agg(countDistinct("postal_code").alias("count")) \
.orderBy("count",ascending=False).show(5)

print('------------------------------------')
print('City which has the most number of users')
df1.select(df1.user_id , df1.user_address.city.alias("city")).groupBy("city").count().orderBy("count",ascending=False).show(5)

print('------------------------------------')
print('Users that have email domain as bizjournals.com')
print(df1.filter(df1.user_email.like("%@bizjournals.com")).count())

print('------------------------------------')
print('Users that have 4 phone numbers mentioned')
print(df1.filter("size(user_phone_numbers) = 4" ).count())

print('------------------------------------')
print('Users do not have any phone number mentioned')
print(df1.filter("size(user_phone_numbers) = 0 or  size(user_phone_numbers) = -1  " ).count())

spark.stop()
