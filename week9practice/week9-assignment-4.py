from pyspark.sql import SparkSession

spark = SparkSession. \
builder. \
appName("week9-assignment-4"). \
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
print('Count of Male / Female from each state who has atleast 1 phone number')

df2 = df1.filter("size(user_phone_numbers) >0" ).withColumn("user_state",col("user_address.state"))

df3 = df2.groupBy("user_state").pivot("user_gender").count().orderBy("user_state")
print('------------------------------------')

df3.write.save('pivot_assignment_result')

print('check hdfs file pivot_assignment_result')


df2.createOrReplaceTempView("users")


spark.sql("""
select * from (
select user_state, user_gender from users 
) 
PIVOT ( count(*) for user_gender in ('Male','Female')
) order by user_state
""").show()
print('------------------------------------')



spark.stop()