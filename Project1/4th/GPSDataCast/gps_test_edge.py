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

@app.route('/gwg_temp', methods=['POST'])
def gwg_temp():
    global bb01, bb02, bb03, bb04, bb05, bb06, bb07

    temp_data = json.loads(request.get_json(silent=True))

    bid = temp_data.get('bid')

    if bid == 'bb01':
        bb01 = temp_data
    elif bid == 'bb02':
        bb02 = temp_data
    elif bid == 'bb03':
        bb03 = temp_data
    elif bid == 'bb04':
        bb04 = temp_data
    elif bid == 'bb05':
        bb05 = temp_data
    elif bid == 'bb06':
        bb06 = temp_data
    elif bid == 'bb07':
        bb07 = temp_data

    return temp_data

@app.route('/get_gps_rdata', methods=['GET'])
def get_get_gps_rdata():
    global bb01, bb02, bb03, bb04, bb05, bb06, bb07

    try:
        bid = request.args['bid']
        if bid == 'bb01':
            if 'bb01' in globals() and bb01:
                return json.dumps(bb01)
            else:
                return missing_data()
        elif bid == 'bb02':
            if 'bb02' in globals() and bb02:
                return json.dumps(bb02)
            else:
                return missing_data()
        elif bid == 'bb03':
            if 'bb03' in globals() and bb03:
                return json.dumps(bb03)
            else:
                return missing_data()
        elif bid == 'bb04':
            if 'bb04' in globals() and bb04:
                return json.dumps(bb04)
            else:
                return missing_data()
        elif bid == 'bb05':
            if 'bb05' in globals() and bb05:
                return json.dumps(bb05)
            else:
                return missing_data()
        elif bid == 'bb06':
            if 'bb06' in globals() and bb06:
                return json.dumps(bb06)
            else:
                return missing_data()
        elif bid == 'bb07':
            if 'bb07' in globals() and bb07:
                return json.dumps(bb07)
            else:
                return missing_data()
        else:
            return f'{bid} 데이터가 없습니다'
    except KeyError:
        res = {
            "code": "0015",
            "message": "필수 파라미터 Missing 오류"
        }
        res_json = json.dumps(res)
        return res_json

    return 'Unknown error occurred'

def missing_data():
    res = {
            "code": "0020",
            "message": "데이터 Missing 오류"
        }
    res_json = json.dumps(res)

    return res_json

app.run(host="123.214.186.162",port=port)

