from flask import Flask, render_template, Response, request, g, jsonify
from flask_cors import CORS, cross_origin
import json
import sqlite3
import datetime
import res

app = Flask(__name__)
CORS(app)
port = 8089

@app.route('/')
def index():
    json_data = request.get_json(silent=True)
    print(json_data)
    return "index"

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

@app.route('/gwg_temp2', methods=['POST'])
def gwg_temp2():
    global bp01, bp02, bp03, bp04, bp05, bp06, bp07

    temp_data = json.loads(request.get_json(silent=True))

    bid = temp_data.get('bid')

    if bid == 'bb01':
        bp01 = temp_data
    elif bid == 'bb02':
        bp02 = temp_data
    elif bid == 'bb03':
        bp03 = temp_data
    elif bid == 'bb04':
        bp04 = temp_data
    elif bid == 'bb05':
        bp05 = temp_data
    elif bid == 'bb06':
        bp06 = temp_data
    elif bid == 'bb07':
        bp07 = temp_data

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
                return res.msg("0020")
        elif bid == 'bb02':
            if 'bb02' in globals() and bb02:
                return json.dumps(bb02)
            else:
                return res.msg("0020")
        elif bid == 'bb03':
            if 'bb03' in globals() and bb03:
                return json.dumps(bb03)
            else:
                return res.msg("0020")
        elif bid == 'bb04':
            if 'bb04' in globals() and bb04:
                return json.dumps(bb04)
            else:
                return res.msg("0020")
        elif bid == 'bb05':
            if 'bb05' in globals() and bb05:
                return json.dumps(bb05)
            else:
                return res.msg("0020")
        elif bid == 'bb06':
            if 'bb06' in globals() and bb06:
                return json.dumps(bb06)
            else:
                return res.msg("0020")
        elif bid == 'bb07':
            if 'bb07' in globals() and bb07:
                return json.dumps(bb07)
            else:
                return res.msg("0020")
        else:
            return res.msg("0020")
    except KeyError:
        return res.msg("0015")

    return res.msg("0012")

@app.route('/get_gps_data', methods=['GET'])
def get_get_gps_data():
    global bp01, bp02, bp03, bp04, bp05, bp06, bp07

    try:
        bid = request.args['bid']
        if bid == 'bb01':
            if 'bb01' in globals() and bp01:
                return json.dumps(bp01)
            else:
                return res.msg("0020")
        elif bid == 'bb02':
            if 'bb02' in globals() and bp02:
                return json.dumps(bp02)
            else:
                return res.msg("0020")
        elif bid == 'bb03':
            if 'bb03' in globals() and bp03:
                return json.dumps(bp03)
            else:
                return res.msg("0020")
        elif bid == 'bb04':
            if 'bb04' in globals() and bp04:
                return json.dumps(bp04)
            else:
                return res.msg("0020")
        elif bid == 'bb05':
            if 'bb05' in globals() and bp05:
                return json.dumps(bp05)
            else:
                return res.msg("0020")
        elif bid == 'bb06':
            if 'bb06' in globals() and bp06:
                return json.dumps(bp06)
            else:
                return res.msg("0020")
        elif bid == 'bb07':
            if 'bb07' in globals() and bp07:
                return json.dumps(bp07)
            else:
                return res.msg("0020")
        else:
            return res.msg("0020")
    except KeyError:
        return res.msg("0015")

    return res.msg("0012")


app.run(host="123.214.186.162",port=port)

