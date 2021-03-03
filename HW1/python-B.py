import json
import sys


with open(sys.argv[1], 'r') as file:
    country = json.load(file)
with open(sys.argv[2], 'r') as file:
    city = json.load(file)
with open(sys.argv[3], 'r') as file:
    countrylanguage = json.load(file)


result = {}
for item in country:
    if item['Continent'] == 'North America':
        result[item['Code']] = {'Name':item['Name'], 'OfficialLanguage':[]}

for item in countrylanguage:
    if item['CountryCode'] in result and item['IsOfficial'] == 'T':
        result[item['CountryCode']]['OfficialLanguage'].append(item['Language'])

# print(json.dumps(result, indent=2))

ansPrint = ''
for key, value in result.items():
    language = ", ".join(value['OfficialLanguage']) if value['OfficialLanguage'] else "None"
    ansPrint += value['Name'] + ', ' + language + '\n'

print(ansPrint)