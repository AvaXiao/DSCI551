from flask import Flask,request
import pymysql
import flask
import json
import datetime
from flask_cors import *


def run(date='2020-11-26'):
    db = pymysql.connect(user='root', password='wildfire', host='db-wildfire.cway8fqttrzk.us-east-2.rds.amazonaws.com', database='wildfire')
    cursor = db.cursor()
    query = "select County, count(*) cnt from instances where record_Date = '{}' and Percent_Contained < 100 group by County order by cnt DESC;".format(date)
    cursor.execute(query)
    results = cursor.fetchall()
    results = json.dumps(results)
    return results


server = Flask(__name__)#创建一个服务
server.debug=False
CORS(server, supports_credentials=True, resources=r'/*')
# cors = CORS(server, resources={r"/api/*": {"origins": "*"}})



@server.route('/data',methods=['get','post'])
def data():    #返回数据
    # response = make_response(jsonify(result_text))
    # response.headers['Access-Control-Allow-Origin'] = '*'

    resp = flask.Response("Foo bar baz")
    resp.headers['Access-Control-Allow-Origin'] = '*'
    resp.headers['Access-Control-Allow-Credentials'] = True
    resp.headers['Access-Control-Allow-Methods'] = 'OPTIONS,HEAD,GET,POST'
    resp.headers['Access-Control-Allow-Headers'] = 'x-requested-with'

    if request.method == 'GET':
        date = datetime.date.today().strftime('%Y-%m-%d')
        return (run(date), 200)

    elif request.method== 'POST':
        date = request.values.get('date')
        return (run(date), 200)



if __name__ == "__main__":
    # server.run(host='0.0.0.0',port=5000)
    server.run(host='127.0.0.1',port=5000)