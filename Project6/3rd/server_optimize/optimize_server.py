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

API_URL = "http://192.168.0.9:5230"

port = "6432"

@ app.route('/optimize_by_weather', methods=['POST'])
def optimize_by_weather():
    try:
        data = request.get_json(silent=True)
        if data is None:
            raise ValueError("No JSON data received")

        json_data = json.loads(data)

        nid = json_data.get('nid')
        created_at = json_data.get('cpu')
        res_class = json_data.get('memory')
        res_confidence = json_data.get('res_confidence')

        if not all([nid, created_at, res_class, res_confidence]):
            raise KeyError("Missing required fields in the request")

        print(f"Node ID: {nid} // Created time: {created_at} // Weather Class: {res_class} // Confidence: {res_confidence}")

        return response.message('0000')

    except json.JSONDecodeError:
        return response.message('0010')

    except KeyError as e:
        return response.message('0015')

    except ValueError as e:
        return response.message('9999')

# - 매초 전달되는 json 파일 저장하기
@app.route('/save_edgeData', methods=['POST'])
def save_edgeData():
    data = request.get_json(silent=True)
    json_data = json.loads(data)

    nid = json_data['nid']
    created_at = json_data['created_at']
    res_class = json_data['res_class']
    res_confidence = json_data['res_confidence']

    print(f"nid : {nid} // time : {created_at} // res_class : {res_class} // res_confidence : {res_confidence}")

    # db 저장되어있는 nid의 노드가 갖고있는 모든 AI 의 class 비교해서
    ai_id_list = requests.get(f"{SETUP_API_URL}/get_deployedAis_by_node?nid={nid}")


    # 일치하면 pass

    # 일치하지 않으면 res_class에 맞는 AI 재배포

    # db에 저장하는 기능 ----- 나중에 구형


    return response.message('0000')

@app.route('/usage', methods=['POST'])
def usage():
    data = request.get_json(silent=True)
    json_data = json.loads(data)

    username = json_data['username']
    cpu_usage = json_data['cpu']
    memory_usage = json_data['memory']
    ai_class = json_data['ai_class']

    print(f"User Name : {username} // AI_class : {ai_class} // CPU Usage : {cpu_usage}% // Memory Usage : {memory_usage}%")

    return "usage"


if __name__ == '__main__':
    app.run(host='0.0.0.0', threaded=True, port=port)
