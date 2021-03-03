import requests


size_download = 0
num_request = 0
url = 'https://ava-551.firebaseio.com/world/'
suffix = '.json'

large_GNP_country = requests.get(url+'country'+suffix+'?orderBy="GNP"&startAt=10001')
num_request += 1
size_download += len(large_GNP_country.content)
large_GNP_country = large_GNP_country.json()


continent = {}
for key, value in large_GNP_country.items():
    region = value["Continent"]
    if not region in continent:
        continent[region] = {'cnt_countries': 1}
    else:
        continent[region]['cnt_countries'] += 1


ansPrint = ''
for key, value in continent.items():
    if value['cnt_countries'] >= 5:
        country = requests.get(url+'country'+suffix+'?orderBy="Continent"&equalTo="'+key+'"')
        num_request += 1
        size_download += len(country.content)
        country = country.json()

        continent[key]['cnt_countries'] = 0
        continent[key]['sum_life_expectancy'] = 0

        for _, value in country.items():
            continent[key]['cnt_countries'] += 1
            continent[key]['sum_life_expectancy'] += value["LifeExpectancy"]

        avg_life_expectancy = continent[key]['sum_life_expectancy'] / continent[key]['cnt_countries']
        ansPrint += key + ', ' + str(avg_life_expectancy) + '\n'


with open('data_Q5.txt','a') as file:
    content = '\nFor C:\nThe number of requests is {}, the size of download data is {} bytes.\n'\
        .format(num_request, size_download)
    file.write(content)

print(ansPrint)