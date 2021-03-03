from pyspark.sql import SparkSession
import pyspark.sql.functions as fc


spark = SparkSession \
    .builder \
    .appName("HW4") \
    .getOrCreate()



country = spark.read.json('country.json')
city = spark.read.json('city.json')
cl = spark.read.json('countrylanguage.json')


tmp = country.join(cl, country.Code == cl.CountryCode)[(cl.Language == 'French') & (cl.IsOfficial == 'T')]
tmp = tmp[[country.Name.alias("Country"), country.Continent]]
tmp.groupBy('Continent').agg(fc.count('*').alias('cnt')).show()