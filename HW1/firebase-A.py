import sys
import requests

# region = "North America"
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
    country_name = value['Name']
    capital_id = value['Capital']

    capital_info = requests.get(url+'city'+suffix+'?orderBy="$key"&equalTo="'+str(capital_id)+'"')
    num_request += 1
    size_download += len(capital_info.content)
    capital_info = capital_info.json()

    capital_name = capital_info[str(capital_id)]['Name']
    ansPrint += country_name + ', ' + capital_name + '\n'


with open('data_Q5.txt','w') as file:
    content = 'For A:\nThe number of requests is {} the size of download data is {} bytes.\n'\
        .format(num_request, size_download)
    file.write(content)


print(ansPrint)