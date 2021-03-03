import sys
import requests

region = sys.argv[1]


num_request = 0
size_download = 0
url = 'https://ava-551.firebaseio.com/world/'
suffix = '.json'

country_nested = requests.get(url+'country_nested'+suffix+'?orderBy="Continent"&equalTo="'+region+'"')
num_request += 1
size_download += len(country_nested.content)
country_nested = country_nested.json()


ansPrint = ''
for key, country_nested_value in country_nested.items():
    country_id = key
    country_name = country_nested_value['Name']

    language = []
    for key, value in country_nested_value['languages'].items():
        if value['IsOfficial'] == 'T':
            language.append(key)

    language = ", ".join(language) if language else "None"
    ansPrint += country_name + ', ' + language + '\n'


with open('data_Q5.txt','a') as file:
    content = '\nFor B use country_nested:\nThe number of requests is {}, the size of download data is {} bytes.\n'\
        .format(num_request, size_download)
    file.write(content)

print(ansPrint)