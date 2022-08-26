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
    json_data = request.get_json(silent=True)
    # print(json_data)
    # did 추출
    # did = json_data['did']
    # 지금은 did 를 사용 안하지만 나중에는 이 아이디로 device ip 를 찾아서 요청해야함
    g.gps_data = json_data

    return "gps data uploaded!"

@app.route('/get_gpsData', methods=['GET'])
def get_gpsData():
    print(g.gps_data)

    return "OK"

app.run(host="123.214.186.162",port=port)

