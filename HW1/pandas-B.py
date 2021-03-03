import pandas as pd
import sys


country = pd.read_json(sys.argv[1])
city = pd.read_json(sys.argv[2])
countrylanguage = pd.read_json(sys.argv[3])

country = country[country['Continent'] == 'North America']
countrylanguage = countrylanguage[countrylanguage['IsOfficial'] == 'T']
countrylanguage = countrylanguage[countrylanguage['CountryCode'].isin(list(country['Code']))]
result = country[['Name']]

result = result.assign(OfficialLanguage = country['Code'].map(
    lambda x: list(countrylanguage[countrylanguage['CountryCode'] == x]['Language']) if x in list(countrylanguage['CountryCode']) else ['None']))

ansPrint = ''
for idx in result.index:
    language = ", ".join(result.loc[idx, 'OfficialLanguage'])
    ansPrint += result.loc[idx, 'Name'] + ', ' + language + '\n'

print(ansPrint)