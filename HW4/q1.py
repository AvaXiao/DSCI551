from pyspark.sql import SparkSession

spark = SparkSession \
    .builder \
    .appName("HW4") \
    .getOrCreate()



country = spark.read.json('country.json')
city = spark.read.json('city.json')
cl = spark.read.json('countrylanguage.json')

country[(country.GNP >= 100000) & (country.GNP <= 500000) & (country.Continent == 'Europe')][['Name']].show()