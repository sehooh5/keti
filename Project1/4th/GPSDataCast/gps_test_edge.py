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

    temp_data = request.get_json(silent=True)

    bid = temp_data['bid']

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
    except KeyError:
        res = {
            "code": "0015",
            "message": "필수 파라미터 Missing 오류"
        }
        res_json = json.dumps(res)
        return res_json

    try:
        if bid == 'bb01':
            if 'bb01' in globals() and bb01:
                return bb01
            else:
                missing_data()
        elif bid == 'bb02':
            if 'bb02' in globals() and bb02:
                return bb02
            else:
                missing_data()
        elif bid == 'bb03':
            if 'bb03' in globals() and bb03:
                return bb03
            else:
                return 'bb03 is empty'
        elif bid == 'bb04':
            if 'bb04' in globals() and bb04:
                return bb04
            else:
                return 'bb04 is empty'
        elif bid == 'bb05':
            if 'bb05' in globals() and bb05:
                return bb05
            else:
                return 'bb05 is empty'
        elif bid == 'bb06':
            if 'bb06' in globals() and bb06:
                return bb06
            else:
                return 'bb06 is empty'
        elif bid == 'bb07':
            if 'bb07' in globals() and bb07:
                return bb07
            else:
                return 'bb07 is empty'
        else:
            return f'{bid} 데이터가 없습니다'
    except KeyError:
        return 'key error'


def missing_data():
    res = {
            "code": "0020",
            "message": "데이터 Missing 오류"
        }
    res_json = json.dumps(res)

    return res_json

app.run(host="123.214.186.162",port=port)

