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

@app.route('/get_gwg', methods=['GET'])
def get_gwg():
    global bb01, bb02, bb03, bb04, bb05, bb06, bb07

    bid = request.args.get('bid')

    if bid == 'bb01':
        return bb01
    elif bid == 'bb02':
        return bb02
    elif bid == 'bb03':
        return bb03
    elif bid == 'bb04':
        return bb04
    elif bid == 'bb05':
        return bb05
    elif bid == 'bb06':
        return bb06
    elif bid == 'bb07':
        return bb07



app.run(host="123.214.186.162",port=port)

