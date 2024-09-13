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

SETUP_API_URL = "http://192.168.0.9:5230"

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
    nip = request.remote_addr
    res = requests.get(f"{SETUP_API_URL}/get_nid_by_ip?nip={nip}")
    if res.status_code == 200:
        json_data = res.json()
        nid = json_data.get('nid')
    else:
        print(f"Failed to retrieve data. Status code: {res.status_code}")

#   Data from Weather AI
    data = request.get_json(silent=True)
    json_data = json.loads(data)

    created_at = json_data['created_at']
    res_class = json_data['res_class']
    res_confidence = json_data['res_confidence']

    print(f"nid : {nid} // time : {created_at} // res_class : {res_class} // res_confidence : {res_confidence}")

#   Data from DB
    res_list = requests.get(f"{SETUP_API_URL}/get_deployedAis_by_node?nid={nid}")
    aid_list_json = res_list.json()
    aid_list = aid_list_json.get('aid_list')
    for aid in aid_list:
        ai_informs = requests.get(f"{SETUP_API_URL}/get_uploadedAiInfo?aid={aid}")
        ai_informs_json = ai_informs.json()
        ai_class = ai_informs_json.get('ai_class')
        filename = ai_informs_json.get('filename')
        print(filename)

        if ai_class == 00:
            print("00",filename)
            pass
        elif ai_class != res_class:
            print(ai_class,filename)
            # 일치하지 않으면 res_class에 맞는 AI 재배포 / aid, nid 필요
            # DB에서 filename이 일치하면서 ai_class가 res_class와 같은 AI의 aid가 필요
            aid = requests.get(f"{SETUP_API_URL}/get_aid_by_fnameAndClass?filename={filename}&class={res_class}")
            print(aid)



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

#     print(f"User Name : {username} // AI_class : {ai_class} // CPU Usage : {cpu_usage}% // Memory Usage : {memory_usage}%")

    return "usage"


if __name__ == '__main__':
    app.run(host='0.0.0.0', threaded=True, port=port)
