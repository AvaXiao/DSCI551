import json
import sys


# with open('country.json', 'r') as file:
#     country = json.loads(file.read().encode('utf-8'))
# with open('city.json', 'r') as file:
#     city = json.loads(file.read().encode('utf-8'))
# with open('countrylanguage.json', 'r') as file:
#     countrylanguage = json.loads(file.read().encode('utf-8'))


with open(sys.argv[1], 'r') as file:
    country = json.load(file)
with open(sys.argv[2], 'r') as file:
    city = json.load(file)
with open(sys.argv[3], 'r') as file:
    countrylanguage = json.load(file)


result = []
for item in country:
    if item['Continent'] == 'North America':
        result.append({'Name':item['Name'], 'Capital':item['Capital']})

# print(json.dumps(result, indent=2))

ansPrint = ''
for idx in range(len(result)):
    for item in city:
        if item['ID'] == result[idx]['Capital']:
            result[idx]['Capital'] = item['Name']
            break
    ansPrint += result[idx]['Name'] + ', ' + result[idx]['Capital'] + '\n'

print(ansPrint)