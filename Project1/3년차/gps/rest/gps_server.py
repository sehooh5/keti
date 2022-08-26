from flask import Flask, render_template, Response, request, g, jsonify
from flask_cors import CORS, cross_origin
import json
import response

app = Flask(__name__)
CORS(app)
port = 8088


@app.route('/')
def index():
    return "index"

@app.route('/gps', methods=['POST'])
def gps():
    global json_data
    json_data = request.get_json(silent=True)

    return "OK"

@app.route('/get_gpsData', methods=['GET'])
def get_gpsData():
    did = request.args.get('did')
    print(did)

    if json_data :
        return json_data
    else:
        return "Null of json_data"

app.run(host="123.214.186.162",port=port)

