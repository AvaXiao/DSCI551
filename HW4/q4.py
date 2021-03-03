from pyspark.sql import SparkSession
import pyspark.sql.functions as fc


spark = SparkSession \
    .builder \
    .appName("HW4") \
    .getOrCreate()



country = spark.read.json('country.json')
city = spark.read.json('city.json')
cl = spark.read.json('countrylanguage.json')


country[(country.GNP > 10000)].groupBy('Continent').agg(fc.mean('LifeExpectancy').alias('avg_life_expectancy')).show()