import pandas as pd
import sys

# country = pd.read_json('country.json')
# city = pd.read_json('city.json')
# countrylanguage = pd.read_json('countrylanguage.json')


country = pd.read_json(sys.argv[1])
city = pd.read_json(sys.argv[2])
countrylanguage = pd.read_json(sys.argv[3])

country = country[country['Continent'] == 'North America']
result = country[['Name', 'Capital']]
city.index = city['ID']

result = result.assign(Capital = country['Capital'].map(lambda x: city.loc[x, 'Name']))
ansPrint = ''
for idx in result.index:
    ansPrint += result.loc[idx, 'Name'] + ', ' + result.loc[idx, 'Capital'] + '\n'

print(ansPrint)