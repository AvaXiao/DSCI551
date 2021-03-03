import mysql.connector
import sys
import json

input_date = "03/2020"
output_file_name = "result.json"

input_date = sys.argv[1]
output_file_name = sys.argv[2]


input_month, input_year = input_date.split('/')
current_date = input_year+"-"+input_month+"%"
if input_month == '01':
    previous_date = str(int(input_year)-1) + "-12%"
else:
    previous_date = input_year+"-"+str(int(input_month)-1).zfill(2)+"%"

cnx = mysql.connector.connect(user='dsci551', password='dsci551', host='127.0.0.1', database='covid19')
cursor = cnx.cursor()
cursor.execute("SELECT VERSION()")


def get_previous_results(attr, table, previous_date, number):
    query = "select {},confirmed, deceased from time{} where date like '{}' order by date desc limit {};".format(attr, table, previous_date, number)

    cursor.execute(query)
    results = cursor.fetchall()

    previous_results = {}
    for idx, result in enumerate(results):
        attr = result[0]
        previous_results[attr] = [int(result[1]), int(result[2])]

    return previous_results


def get_results(attr, table, current_date, output, previous_date):
    query_count = 'select count({}) from time{} group by date limit 1;'.format(attr, table, current_date)
    cursor.execute(query_count)
    number = cursor.fetchall()[0][0]

    query = "select {},confirmed, deceased from time{} where date like '{}' order by date desc limit {};".format(attr, table, current_date, number)
    cursor.execute(query)
    results = cursor.fetchall()
    previous_results = get_previous_results(attr, table, previous_date, number)

    if previous_results:
        for idx, result in enumerate(results):
            attr = result[0]
            output[table][attr] = output[table].get(attr, {})
            output[table][attr]['confirmed'] = int(result[1]) - previous_results[attr][0]
            output[table][attr]['deceased'] = int(result[2]) - previous_results[attr][1]
    else:
        for idx, result in enumerate(results):
            attr = result[0]
            output[table][attr] = output[table].get(attr, {})
            output[table][attr]['confirmed'] = int(result[1])
            output[table][attr]['deceased'] = int(result[2])

    return output



output = {'gender':{}, 'age':{}, 'province':{}}
output = get_results('sex', 'gender', current_date, output, previous_date)
output = get_results('age', 'age', current_date, output, previous_date)
output = get_results('province', 'province', current_date, output, previous_date)
output_json = json.dumps(output, indent=4)

file = open(output_file_name, 'w')
file.write(output_json)
file.close()


cursor.close()
cnx.close()