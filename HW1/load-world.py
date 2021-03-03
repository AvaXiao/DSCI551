import sys
import json
import requests


with open(sys.argv[1], 'r') as file:
    country = json.loads(file.read().encode('utf-8'))
with open(sys.argv[2], 'r') as file:
    city = json.loads(file.read().encode('utf-8'))
with open(sys.argv[3], 'r') as file:
    countrylanguage = json.loads(file.read().encode('utf-8'))


url = 'https://ava-551.firebaseio.com/'
suffix = '.json'

tmp_country = {}
for item in country:
    code = item.pop('Code')
    tmp_country[code] = item
requests.put(url + suffix, '{"world":{"country":'+json.dumps(tmp_country)+'}}')

tmp_city = {}
url = 'https://ava-551.firebaseio.com/world'
for item in city:
    id = item.pop('ID')
    tmp_city[id] = item
requests.patch(url + suffix, '{"city":'+json.dumps(tmp_city)+'}')

tmp_language = {}
for item in countrylanguage:
    code = item.pop('CountryCode')
    language = item.pop('Language')
    tmp_language[code] = tmp_language.get(code, {})
    tmp_language[code][language] = item
requests.patch(url + suffix, '{"countrylanguage":'+json.dumps(tmp_language).replace('[','').replace(']','')+'}')

tmp_nested = tmp_country.copy()
for key, value in tmp_nested.items():
    try:
        tmp_nested[key]['languages'] = tmp_language[key]
    except:
        tmp_nested[key]['languages'] = "null"
requests.patch(url + suffix, '{"country_nested":'+json.dumps(tmp_nested).replace('[','').replace(']','')+'}')