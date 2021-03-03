import json
import sys


with open(sys.argv[1], 'r') as file:
    country = json.load(file)
with open(sys.argv[2], 'r') as file:
    city = json.load(file)
with open(sys.argv[3], 'r') as file:
    countrylanguage = json.load(file)

continent = {}
for item in country:
    region = item["Continent"]
    if not region in continent:
        continent[region] = {'cnt_GNP': 0, 'cnt_countries': 1, 'sum_life_expectancy': item["LifeExpectancy"]}
    else:
        continent[region]['cnt_countries'] += 1
        continent[region]['sum_life_expectancy'] += item["LifeExpectancy"]
    if item['GNP'] > 1e4:
        if region in continent:
            continent[region]['cnt_GNP'] += 1

del_key = []
for key, value in continent.items():
    if value['cnt_GNP'] < 5:
        del_key.append(key)
_ = [continent.pop(key) for key in del_key]

for key, value in continent.items():
    continent[key]['avg_life_expectancy'] = continent[key]['sum_life_expectancy'] / continent[key]['cnt_countries']

# print(json.dumps(continent, indent=2))

ansPrint = ''
for key, value in continent.items():
    ansPrint += key + ', ' + str(value['avg_life_expectancy']) + '\n'

print(ansPrint)