import sys
import requests

region = sys.argv[1]


num_request = 0
size_download = 0
url = 'https://ava-551.firebaseio.com/world/'
suffix = '.json'

country = requests.get(url+'country'+suffix+'?orderBy="Continent"&equalTo="'+region+'"')
num_request += 1
size_download += len(country.content)
country = country.json()


ansPrint = ''
for key, value in country.items():
    country_id = key
    country_name = value['Name']

    languages = requests.get(url+'countrylanguage'+suffix+'?orderBy="$key"&equalTo="'+str(country_id)+'"')
    num_request += 1
    size_download += len(languages.content)
    languages = languages.json()

    language = []
    for key, value in languages[country_id].items():
        if value['IsOfficial'] == 'T':
            language.append(key)

    language = ", ".join(language) if language else "None"
    ansPrint += country_name + ', ' + language + '\n'


with open('data_Q5.txt','a') as file:
    content = '\nFor B use countrylanguage:\nThe number of requests is {}, the size of download data is {} bytes.\n'\
        .format(num_request, size_download)
    file.write(content)

print(ansPrint)