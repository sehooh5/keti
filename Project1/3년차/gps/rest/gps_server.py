from flask import Flask, render_template, Response, request, jsonify
from flask_cors import CORS, cross_origin
import json
import requests
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
    # did 추출
    did = json_data['did']
    # 지금은 did 를 사용 안하지만 나중에는 이 아이디로 device ip 를 찾아서 요청해야함
    dip = "http://192.168.225.27:5885"
    res = requests.get(f"{dip}/get_gpsInfo")

    return res

app.run(host="123.214.186.162",port=port)

