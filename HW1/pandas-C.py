import pandas as pd
import sys


country = pd.read_json(sys.argv[1])
city = pd.read_json(sys.argv[2])
countrylanguage = pd.read_json(sys.argv[3])

continent = country[country['GNP'] > 1e4]['Continent']
continent = continent.value_counts() >= 5
continent = list(continent[continent == True].index)

country = country[country['Continent'].isin(continent)]
result = country.groupby(['Continent']).mean()['LifeExpectancy']

ansPrint = ''
for idx in result.index:
    ansPrint += idx + ', ' + str(result.loc[idx]) + '\n'

print(ansPrint)

