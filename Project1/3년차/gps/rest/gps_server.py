from flask import Flask, render_template, Response, request, jsonify
from flask_cors import CORS, cross_origin
import json
import requests_test
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
    print(json_data)
    # 지금은 did 를 사용 안하지만 나중에는 이 아이디로 device ip 를 찾아서 요청해야함


    return res

app.run(host="123.214.186.162",port=port)

