#!/usr/bin/env python
## app.py 기반 master 에서 실행되는 서버
from importlib import import_module
from typing import List
from flask import Flask, render_template, Response, request, jsonify
from flask_cors import CORS, cross_origin
from models import db, AI_uploaded, AI_deployed, Node_info
import json
import requests
import os
import response
import string
import random_string


app = Flask(__name__)
app.config['JSON_AS_ASCII'] = False  # jsonify 한글깨짐 해결
CORS(app)

# 랜덤한 문자열 생성기
_LENGTH = 4
string_pool = string.ascii_letters + string.digits

MASTER_API_URL = "http://192.168.0.4:5231"
OPTIMIZE_API_URL = "http://192.168.0.14:6432"

port = "5230"

@ app.route('/ping_to_master', methods=['GET'])
def ping_to_master():
    requests.get(f"{MASTER_API_URL}/ping_from_setup")

    return response.message('0000')

@ app.route('/request_upload_edgeAi', methods=['POST'])
def request_upload_edgeAi():
    json_data = request.get_json(silent=True)

    aid = random_string.generate(4)
    filename = json_data['filename']
    filename = filename.split('-')[0]
    version = json_data['version']
    ai_class = json_data['ai_class']


    ai_info = AI_uploaded(aid=aid, filename=filename, version=version,
               ai_class=ai_class)
    db.session.add(ai_info)
    db.session.commit()
    print(f"Uploaded AI Data saved in Database! ---- AI ID :{aid}")

    data = {
        "aid": aid,
        "filename": filename,
        "version": version,
        "ai_class": ai_class
    }

    requests.post(f"{MASTER_API_URL}/upload_edgeAi", json=data)

    # 최적화 서버에 버전정보 비교 trigger
    requests.post(f"{OPTIMIZE_API_URL}/optimize_by_version", json=data)

    return response.message('0000')


@ app.route('/request_remove_edgeAi', methods=['POST'])
def request_remove_edgeAi():
    json_data = request.get_json(silent=True)

    aid = json_data['aid']

    data = {
        "aid": aid
    }
    requests.post(f"{MASTER_API_URL}/remove_edgeAi", json=data)

    ai_info = db.session.query(AI_uploaded).filter(AI_uploaded.aid == aid).first()
    db.session.delete(ai_info)
    db.session.commit()

    return response.message('0000')

@ app.route('/request_deploy_aiToDevice', methods=['POST'])
def request_deploy_aiToDevice ():
    json_data = request.get_json(silent=True)

    aid = json_data['aid']
### 임시로 ni01 ===  intellivix-worker-01 으로 입력중
    nid = json_data['nid']


    ai_deployed_info = AI_deployed(aid=aid, nid=nid)
    db.session.add(ai_deployed_info)
    db.session.commit()
    print(f"deployed AI Data saved in Database! ---- AI ID :{aid} / Node ID : {nid}")

    data = {
        "aid": aid,
        "nid": nid
    }

    requests.post(f"{MASTER_API_URL}/deploy_aiToDevice", json=data)

    return response.message('0000')

@ app.route('/request_undeploy_aiFromDevice', methods=['POST'])
def request_undeploy_aiFromDevice():
    json_data = request.get_json(silent=True)

    aid = json_data['aid']
### 임시로 ni01 ===  intellivix-worker-01 으로 입력중
    nid = json_data['nid']

    data = {
        "aid": aid,
        "nid": nid
    }
    requests.post(f"{MASTER_API_URL}/undeploy_aiFromDevice", json=data)

    ai_deployed_info = db.session.query(AI_deployed).filter(AI_deployed.nid == nid, AI_deployed.aid == aid).first()
    db.session.delete(ai_deployed_info)
    db.session.commit()

    return response.message('0000')

@ app.route('/get_uploadedAiInfo', methods=['GET'])
def get_uploadedAiInfo():
    aid = request.args.get('aid')

    # DB 정보 획득
    ai_info = db.session.query(AI_uploaded).filter(AI_uploaded.aid == aid).first()

    data = {
        "code":"0000",
        "message":"처리 성공",
        "aid": ai_info.aid,
        "filename": ai_info.filename,
        "version": ai_info.version,
        "ai_class": ai_info.ai_class
    }
    json_data = json.dumps(data)

    return json_data

@ app.route('/get_deployedAis_by_node', methods=['GET'])
def get_deployedAis_by_node():
    nid = request.args.get('nid')

    # DB 정보 획득
    ai_deployed_list = db.session.query(AI_deployed.aid).filter(AI_deployed.nid == nid).all()
    aid_list = [result.aid for result in ai_deployed_list]

    data = {"aid_list": aid_list}
    json_data = json.dumps(data)

    return json_data

@ app.route('/get_deployedNodes_by_aid', methods=['GET'])
def get_deployedNodes_by_aid():
    aid = request.args.get('aid')

    # DB 정보 획득
    nid_deployed_list = db.session.query(AI_deployed.nid).filter(AI_deployed.aid == aid).all()
    nid_list = [result.nid for result in nid_deployed_list]

    data = {"nid_list": nid_list}
    json_data = json.dumps(data)

    return json_data

@app.route('/get_nid_by_ip', methods=['GET'])
def get_node_id():
    nip = request.args.get('nip')

    # nip에 해당하는 nid 찾기
    node = db.session.query(Node_info).filter(Node_info.nip == nip).first()

    if node:
        return jsonify({"nid": node.nid}), 200
    else:
        return jsonify({"error": "Node not found"}), 404

@app.route('/get_aid_by_fnameAndClass', methods=['GET'])
def get_aid_by_fnameAndClass():
    filename = request.args.get('filename')
    ai_class = request.args.get('class')

    ai_inform = db.session.query(AI_uploaded.aid).filter(AI_uploaded.filename == filename,
    AI_uploaded.ai_class == ai_class).first()


    if ai_inform:
        return jsonify({"aid": ai_inform.aid}), 200
    else:
        return jsonify({"error": "aid not found"}), 404

@app.route('/get_aid_by_fnameAndClass_not_version', methods=['GET'])
def get_aid_by_fnameAndClass_not_version():
    filename = request.args.get('filename')
    ai_class = request.args.get('class')
    not_version = request.args.get('version')

    ai_inform = db.session.query(AI_uploaded.aid).filter(AI_uploaded.filename == filename,
    AI_uploaded.ai_class == ai_class,AI_uploaded.version != not_version).first()


    if ai_inform:
        return jsonify({"aid": ai_inform.aid}), 200
    else:
        return jsonify({"error": "aid not found"}), 404

# DB
basdir = os.path.abspath(os.path.dirname(__file__))
dbfile = os.path.join(basdir, 'db.sqlite')

app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///' + dbfile
app.config['SQLALCHEMY_COMMIT_ON_TEARDOWN'] = True
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
app.config['SECRET_KEY'] = 'jqiowejrojzxcovnklqnweiorjqwoijroi'

db.init_app(app)
app.app_context().push()
db.create_all()

if __name__ == '__main__':
    app.run(host='0.0.0.0', threaded=True, port=port)
