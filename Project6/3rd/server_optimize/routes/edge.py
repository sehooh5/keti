from flask import Blueprint, request
import requests
import json

edge_bp = Blueprint('edge', __name__)

@edge_bp.route('/', methods=['POST'])
def save_edgeData():
    nip = request.remote_addr
    res = requests.get(f"http://192.168.0.9:5230/get_nid_by_ip?nip={nip}")
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