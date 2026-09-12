from pyspark.sql.functions import udf
from pyspark.sql.types import *

@udf(returnType=FloatType())
def inr_to_usd(inr):
    """ INR to USD. 1 UDS = 88.7 rs"""
    return inr/88.72
