import mysql.connector
import sys

table = "patientinfo"
attrs = "patient_id"

table = sys.argv[1]
attrs = sys.argv[2]


cnx = mysql.connector.connect(user='dsci551', password='dsci551', host='127.0.0.1', database='covid19')
cursor = cnx.cursor()

query = "select {},count({}) times from covid19.{} group by {} order by times desc limit 5;".format(attrs, attrs.split(',')[0], table, attrs)
cursor.execute(query)
results = cursor.fetchall()

if results[0][-1] > 1:
    for result in results:
        if result[-1] > 1:
            print(','.join([str(x) for x in result]))
        else:
            break
else:
    print('yes')


cursor.close()
cnx.close()