#!/usr/bin/env python
## app.py 기반 master 에서 실행되는 서버
from importlib import import_module
from typing import List
from flask import Flask, render_template, Response, request, jsonify
from flask_cors import CORS, cross_origin
import json
import requests
import os
import response
import string

app = Flask(__name__)
app.config['JSON_AS_ASCII'] = False  # jsonify 한글깨짐 해결
CORS(app)

# 랜덤한 문자열 생성기
_LENGTH = 4
string_pool = string.ascii_letters + string.digits

API_URL = "http://123.214.186.244:4880"

port = "6432"

@ app.route('/optimize_by_weather', methods=['POST'])
def optimize_by_weather():

    # 환경정보 데이터 받기
    data = request.get_json(silent=True)
    json_data = json.loads(data)

    "nid": "0xn1",
    "created_at": "2024-07-25T12:34:56Z",
    "res_class": "4",
    "res_confidence": 0.7
    nid = json_data['nid']
    created_at = json_data['cpu']
    res_class = json_data['memory']
    res_confidence = json_data['res_confidence']

    print(f"Node ID : {nid} // Created time : {created_at} // Weather Class : {res_class} //  Confidence : {res_confidence} ")

    return res

if __name__ == '__main__':
    app.run(host='0.0.0.0', threaded=True, port=port)
