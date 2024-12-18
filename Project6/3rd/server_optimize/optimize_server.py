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
app.config['JSON_AS_ASCII'] = False
CORS(app)

SETUP_API_URL = "http://192.168.0.9:5230"

port = "6432"

@ app.route('/optimize_by_version', methods=['POST'])
def optimize_by_version():
    try:
        data = request.get_json(silent=True)
        if data is None:
            raise ValueError("No JSON data received")

        # 신버전 AI
        newAI_aid = data.get('aid')
        newAI_filename = data.get('filename')
        newAI_version = data.get('version')
        newAI_ai_class = data.get('ai_class')

        # 구버전 AI
        aid_data = requests.get(f"{SETUP_API_URL}/get_aid_by_fnameAndClass_not_version?filename={newAI_filename}&class={newAI_ai_class}&version={newAI_version}")
        aid_json_data = aid_data.json()
        uploaded_aid = aid_json_data.get('aid')
        uploaded_ai_data = requests.get(f"{SETUP_API_URL}/get_uploadedAiInfo?aid={uploaded_aid}")
        uploaded_ai_json_data = uploaded_ai_data.json()
        uploaded_ai_version = uploaded_ai_json_data.get('version')
        uploaded_ai_filename = uploaded_ai_json_data.get('filename')
        uploaded_ai_class = uploaded_ai_json_data.get('ai_class')

        if int(uploaded_ai_version) < int(newAI_version):
            res_list = requests.get(f"{SETUP_API_URL}/get_deployedNodes_by_aid?aid={uploaded_aid}")
            nid_list_json = res_list.json()
            nid_list = nid_list_json.get('nid_list')
            #nid list 존재할때만 undeploy 해주는거 추가해야함
            if nid_list:
                print("nid_list : ", nid_list)
                for nid in nid_list:
                    old_data = {
                        "aid": uploaded_aid,
                        "nid": nid
                    }

                    # 구버전 삭제
                    print(f"Delete [AI : {uploaded_ai_filename} / Version : {uploaded_ai_version}]......")
                    requests.post(f"{SETUP_API_URL}/request_undeploy_aiFromDevice", json=old_data)

                    # newAI_version 배포
                    data_optimized = {
                        "aid": newAI_aid,
                        "nid": nid
                    }
                    print(f"Deploy a new [AI : {newAI_filename} / Version : {newAI_version}]......")
                    requests.post(f"{SETUP_API_URL}/request_deploy_aiToDevice", json=data_optimized)
            else:
                print("nid_list가 없습니다.")
            # 업로드된 구버전 AI 이미지 삭제
            requests.post(f"{SETUP_API_URL}/request_remove_edgeAi", json=old_data)

        return response.message('0000')

    except json.JSONDecodeError:
        return response.message('0010')

    except KeyError as e:
        return response.message('0015')

    except ValueError as e:
        return response.message('9999')

@app.route('/optimize_by_weather', methods=['POST'])
def optimize_by_weather():
    nip = request.remote_addr
    res = requests.get(f"{SETUP_API_URL}/get_nid_by_ip?nip={nip}")
    if res.status_code == 200:
        json_data = res.json()
        nid = json_data.get('nid')
    else:
        print(f"Failed to retrieve data. Status code: {res.status_code}")

#   Data from Weather AI
    data = request.get_json(silent=True)
    created_at = data['created_at']
    res_class = data['res_class']
    res_confidence = data['res_confidence']

    print(f"res_class : {res_class}, res_confidence : {res_confidence}, created_at : {created_at}")

#   Data from DB
    res_list = requests.get(f"{SETUP_API_URL}/get_deployedAis_by_node?nid={nid}")
    if res_list.status_code != 200:
        print(f"Failed to retrieve deployed AIs. Status code: {res_list.status_code}")
        return response.message("Failed to retrieve deployed AIs")

    aid_list_json = res_list.json()
    aid_list = aid_list_json.get('aid_list')
    for aid in aid_list:
        ai_informs = requests.get(f"{SETUP_API_URL}/get_uploadedAiInfo?aid={aid}")
        if ai_informs.status_code != 200:
            print(f"Failed to retrieve AI info for aid {aid}. Status code: {ai_informs.status_code}")
            continue

        ai_informs_json = ai_informs.json()
        ai_class = ai_informs_json.get('ai_class')
        filename = ai_informs_json.get('filename')

        if ai_class != "00" and ai_class != res_class:
            print(f"[AI : {filename} / Class : {ai_class}] AI Optimizing.........")
            data = {
                "aid": aid,
                "nid": nid
            }
            print(f"Delete [AI : {filename} / Class : {ai_class}]......")
            requests.post(f"{SETUP_API_URL}/request_undeploy_aiFromDevice", json=data)

            # 최적화 AI
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
    version = json_data['version']

    if ai_class == "01":
        weather_info = "맑음"
    elif ai_class == "02":
        weather_info = "비"

    print(f"User : {username} / CPU : {cpu_usage} / MEM : {memory_usage} / Weather : {weather_info} / Version : {version}")

    return "usage"


if __name__ == '__main__':
    app.run(host='0.0.0.0', threaded=True, port=port)
