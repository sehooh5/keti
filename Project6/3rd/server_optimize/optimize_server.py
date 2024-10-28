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


SETUP_API_URL = "http://192.168.0.9:5230"

port = "6432"

# 현재 안쓰고잇음
# @ app.route('/optimize_by_weather', methods=['POST'])
# def optimize_by_weather():
#     try:
#         data = request.get_json(silent=True)
#         if data is None:
#             raise ValueError("No JSON data received")
#
#         json_data = json.loads(data)
#
#         nid = json_data.get('nid')
#         created_at = json_data.get('cpu')
#         res_class = json_data.get('memory')
#         res_confidence = json_data.get('res_confidence')
#
#         if not all([nid, created_at, res_class, res_confidence]):
#             raise KeyError("Missing required fields in the request")
#
#         print(f"Node ID: {nid} // Created time: {created_at} // Weather Class: {res_class} // Confidence: {res_confidence}")
#
#         return response.message('0000')
#
#     except json.JSONDecodeError:
#         return response.message('0010')
#
#     except KeyError as e:
#         return response.message('0015')
#
#     except ValueError as e:
#         return response.message('9999')

@ app.route('/optimize_by_version', methods=['POST'])
def optimize_by_version():
    try:
        data = request.get_json(silent=True)
        if data is None:
            raise ValueError("No JSON data received")

        # 신버전 ai
        newAI_json_data = json.loads(data)
        newAI_aid = newAI_json_data.get('aid')
        newAI_filename = newAI_json_data.get('filename')
        newAI_version = newAI_json_data.get('version')
        newAI_ai_class = newAI_json_data.get('ai_class')

        # 구버전 AI : 등록/설정서버에 업로드된 AI중에 새버전 AI와 같은 filename, ai_class 를 갖는 aid를 찾고
        aid_data = requests.get(f"{SETUP_API_URL}/get_aid_by_fnameAndClass_not_version?filename={filename}&class={res_class}&version={newAI_version}")
        aid_json_data = json.loads(aid_data)
        uploaded_aid = aid_json_data.get('aid')
        uploaded_ai_data = requests.get(f"{SETUP_API_URL}/get_uploadedAiInfo?aid={uploaded_aid}")
        uploaded_ai_json_data = uploaded_ai_data.json()
        uploaded_ai_version = uploaded_ai_json_data.get('version')
        uploaded_ai_filename = uploaded_ai_json_data.get('filename')
        uploaded_ai_class = uploaded_ai_json_data.get('ai_class')

        if int(uploaded_ai_version) < int(newAI_version):
            res_list = requests.get(f"{SETUP_API_URL}/get_deployedNodes_by_aid?aid={uploaded_ai_version}")
            nid_list_json = res_list.json()
            nid_list = nid_list_json.get('mid_list')
            for nid in nid_list:
                old_data = {
                    "aid": uploaded_aid,
                    "nid": nid
                }

                # 구버전 삭제
                print(f"Delete [AI : {uploaded_ai_filename} / Version : {uploaded_ai_version}]......")
                requests.post(f"{SETUP_API_URL}/request_undeploy_aiFromDevice", json=data)

                # newAI_version 배포
                data_optimized = {
                    "aid": newAI_aid,
                    "nid": nid
                }
                print(f"Deploy a new [AI : {newAI_filename} / Version : {newAI_version}]......")
                requests.post(f"{SETUP_API_URL}/request_deploy_aiToDevice", json=data_optimized)

            # 업로드된 구버전 AI 이미지 삭제
            requests.post(f"{SETUP_API_URL}/request_remove_edgeAi", json=old_data)

        return response.message('0000')

    except json.JSONDecodeError:
        return response.message('0010')

    except KeyError as e:
        return response.message('0015')

    except ValueError as e:
        return response.message('9999')

# optimize_by_weather
@app.route('/optimize_by_weather', methods=['POST'])
def optimize_by_weather():
    nip = request.remote_addr
    res = requests.get(f"{SETUP_API_URL}/get_nid_by_ip?nip={nip}")
    if res.status_code == 200:
        json_data = res.json()
        nid = json_data.get('nid')
    else:
        print(f"Failed to retrieve data. Status code: {res.status_code}")
    print(nid)

#   Data from Weather AI
    data = request.get_json(silent=True)

    created_at = data['created_at']
    res_class = data['res_class']
    res_confidence = data['res_confidence']

    print(f"{created_at}, {res_class}, {res_confidence}")

#   Data from DB
    res_list = requests.get(f"{SETUP_API_URL}/get_deployedAis_by_node?nid={nid}")
    aid_list_json = res_list.json()
    aid_list = aid_list_json.get('aid_list')
    for aid in aid_list:
        ai_informs = requests.get(f"{SETUP_API_URL}/get_uploadedAiInfo?aid={aid}")
        ai_informs_json = ai_informs.json()
        ai_class = ai_informs_json.get('ai_class')
        filename = ai_informs_json.get('filename')

        if ai_class != "00" and ai_class != res_class:
            print(f"[AI : {filename} / Class : {ai_class}] AI Optimizing.........")
            # res_class에 맞는 AI 재배포 / aid, nid 필요
            # 현재 배포된 AI 삭제
            data = {
                "aid": aid,
                "nid": nid
            }
            print(f"Delete [AI : {filename} / Class : {ai_class}]......")
            requests.post(f"{SETUP_API_URL}/request_undeploy_aiFromDevice", json=data)

            # 최적화 AI ID = aid_optimized
            aid_data = requests.get(f"{SETUP_API_URL}/get_aid_by_fnameAndClass?filename={filename}&class={res_class}")
            aid_json = aid_data.json()
            aid_optimized = aid_json.get('aid')
            print(f"aid_optimized : {aid_optimized}")

            data_optimized = {
                "aid": aid_optimized,
                "nid": nid
            }
            print(f"Deploy a new [AI : {filename} / Class : {res_class}]......")
            requests.post(f"{SETUP_API_URL}/request_deploy_aiToDevice", json=data_optimized)

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
