#!/usr/bin/env python
## app.py 기반 master 에서 실행되는 서버
from importlib import import_module
from typing import List
from flask import Flask, render_template, Response, request, jsonify
from flask_cors import CORS, cross_origin
from models import db, AI_uploaded, AI_deployed
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

    print(f"Print out Json data : {data}")

    requests.post(f"{MASTER_API_URL}/upload_edgeAi", json=data)

    return response.message('0000')


@ app.route('/request_remove_edgeAi', methods=['POST'])
def request_remove_edgeAi():
    json_data = request.get_json(silent=True)

    aid = json_data['aid']

    # DB 삭제
    ai_info = db.session.query(AI_uploaded).filter(AI_uploaded.aid == aid).first()
#     db.session.delete(ai_info)
#     db.session.commit()

    data = {
        "aid": aid
    }

    # Master 서버에 요청
    requests.post(f"{MASTER_API_URL}/remove_edgeAi", json=data)

    return response.message('0000')

@ app.route('/request_deploy_aiToDevice ', methods=['POST'])
def request_deploy_aiToDevice ():
    json_data = request.get_json(silent=True)

    option = requests.post(
        f"http://{edge_ip}:{nodeport}/connect", data=json_data)
    requests.post(f"{MASTER_API_URL}/upload_edgeAi")

    # DB 저장


    return response.message('0000')

@ app.route('/request_undeploy_aiFromDevice', methods=['POST'])
def request_undeploy_aiFromDevice():
    json_data = request.get_json(silent=True)

    option = requests.post(
        f"http://{edge_ip}:{nodeport}/connect", data=json_data)
    requests.post(f"{MASTER_API_URL}/upload_edgeAi")

    # DB 저장


    return response.message('0000')

@ app.route('/get_uploadedAiInfo', methods=['GET'])
def get_uploadedAiInfo():
    aid = request.args.get('aid')

    # DB 정보 획득
    ai_info = db.session.query(AI_uploaded).filter(AI_uploaded.aid == aid).first()
    print(f"AI ID: {ai_info.aid}")
    print(f"Filename: {ai_info.filename}")
    print(f"Version: {ai_info.version}")
    print(f"AI Class: {ai_info.ai_class}")

    return response.message('0000')

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
