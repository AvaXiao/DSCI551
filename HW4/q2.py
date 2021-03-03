from pyspark.sql import SparkSession




spark = SparkSession \
    .builder \
    .appName("HW4") \
    .getOrCreate()



country = spark.read.json('country.json')
city = spark.read.json('city.json')
cl = spark.read.json('countrylanguage.json')


tmp = country.join(city, country.Capital == city.ID)[(country.Continent == 'North America')]
tmp[[country.Name.alias("Country"), city.Name.alias("Capital")]].orderBy(['Country'], ascending=[True]).show(10)