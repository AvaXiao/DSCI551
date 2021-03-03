import mysql.connector
import sys

patient_id = "5000000022"
patient_id = sys.argv[1]


cnx = mysql.connector.connect(user='dsci551', password='dsci551', host='127.0.0.1', database='covid19')
cursor = cnx.cursor()
output = [patient_id]

flag = True
circle = False
while flag:
    query = "select infected_by from patientinfo where patient_id={};".format(patient_id)
    cursor.execute(query)
    results = cursor.fetchall()
    if results:
        patient_id = results[0][0].split(',')[0]
        if patient_id in output:
            circle = True
            flag = False
        if patient_id:
            output.append(patient_id)
        else:
            flag = False
    else:
        flag = False

if circle:
    print('Cycle found: '+','.join(output))
else:
    print(','.join(output))

cursor.close()
cnx.close()