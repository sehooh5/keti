from flask import Flask, render_template, Response, request, g, jsonify
from flask_cors import CORS, cross_origin
import json
import sqlite3
import datetime

app = Flask(__name__)
CORS(app)
port = 8089

# DB 생성 (오토 커밋)
# conn = sqlite3.connect("gwg_test_SA_1.db", isolation_level=None, check_same_thread=False)

# 커서 획득
# c = conn.cursor()

@app.route('/')
def index():
    json_data = request.get_json(silent=True)
    print(json_data)
    return "index"

@app.route('/get_gwgData', methods=['GET'])
def get_gwgData():
    global gwg_data
    j_data = json.dumps(gwg_data)

    return j_data

# 0517 gps 임시 데이터
@app.route('/gwg_temp', methods=['POST'])
def gwg_temp():
    global temp_data
    temp_data = request.get_json(silent=True)
    encoded_data = temp_data['gps_raw_data']
    print(bytes.fromhex(encoded_data))
#     print(temp_data)
    return temp_data

# 1124 // temp data get요청으로 gwg json data 리턴
@app.route('/get_gwg', methods=['GET'])
def get_gwg():
    global temp_data
    j_data = json.dumps(temp_data)

    return j_data


app.run(host="123.214.186.162",port=port)

