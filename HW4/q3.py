from pyspark.sql import SparkSession
import pyspark.sql.functions as f


spark = SparkSession \
    .builder \
    .appName("HW4") \
    .getOrCreate()



country = spark.read.json('country.json')
city = spark.read.json('city.json')
cl = spark.read.json('countrylanguage.json')


tmp = country.join(cl, country.Code == cl.CountryCode)[(country.Continent == 'North America') & (cl.IsOfficial == 'T')]
tmp = tmp[[country.Name.alias("Country"), cl.Language.alias("languages")]]
tmp.groupby("Country").agg(f.concat_ws(", ", f.collect_list(tmp.languages)).alias("official_languages")).orderBy(['Country'], ascending=[True]).limit(10).show()