#!/usr/bin/env python
## app.py 기반 master 에서 실행되는 서버
from importlib import import_module
from typing import List
from flask import Flask, render_template, Response, request, jsonify
from flask_cors import CORS, cross_origin
import json
import requests
import os
# from models import db, SW_up, Server, Server_SW
import response
import string
import random
import paramiko
import time
import subprocess
import zipfile
import datetime
import sys
import shutil
# docker folder
from docker import getImageTag as git
# k8s folder
from k8s import deployment_maker as dm
from k8s import monitoring_maker as mm
from k8s import node_selector as ns

os.environ['KUBECONFIG'] = '/home/keti-jx-02/.kube/config'

app = Flask(__name__)
app.config['JSON_AS_ASCII'] = False  # jsonify 한글깨짐 해결
CORS(app)

# 다른 서버에 명령 보낼때 사용
cli = paramiko.SSHClient()
cli.set_missing_host_key_policy(paramiko.AutoAddPolicy)

# 랜덤한 문자열 생성기
_LENGTH = 4
string_pool = string.ascii_letters + string.digits


# k8s 기능 체크
@ app.route('/check_k8s_node', methods=['GET'])
def check_k8s_node():
    s_name = os.system("echo $HOME")
    print(s_name)

    return response.message("0000")


SETUP_API_URL = "http://192.168.0.9:5230"
private_repo = "192.168.0.4:5000"

# IP 주소
ips = subprocess.check_output("hostname -I", shell=True).decode('utf-8')
ip = ips.split(' ')[0]
port = "5231"

# host name
user_name = os.getlogin()
print(user_name)

# file path
file_path = f"/home/{user_name}/"

#Docker Login 실행
# Docker ID
docker_id = "sehooh5"
try:
    print("Docker login status is Checking...")
    subprocess.check_output("docker info | grep Username", shell=True).decode('utf-8')
except subprocess.CalledProcessError:
    print("Docker login status : none")
    # docker login 실행
    print("Docker login..")
    os.system(f"docker login -u {docker_id} -p @Dhtpgh1234")


@ app.route('/')
def index():
    return "접속 완료"

@ app.route('/ping_from_setup', methods=['GET'])
def ping_from_setup():
    print("Ping Alarm by Setup Server!")

    return response.message('0000')

@ app.route('/upload_edgeAi', methods=['POST'])
def upload_edgeAi():
    func = sys._getframe().f_code.co_name
    print(datetime.datetime.now().strftime(
        "%c")[:-4], f"{func}: start uploading a new software")
    json_data = request.get_json(silent=True)

    print(f"print json_data : {json_data}")
    if json_data == None:
        return response.message("0015")

    aid = json_data['aid']
    filename = json_data['filename']
    version = json_data['version']
    ai_class = json_data['ai_class'] # 추가

    fname = filename.split('-')[0]
    print(datetime.datetime.now().strftime(
    "%c")[:-4], f"{func}: software name: {fname}")

    print(datetime.datetime.now().strftime("%c")[:-4], f"{func}: docker image building...")
    print(f"명령어확인 ----- docker build -t {private_repo}/{fname}-{ai_class}:{version} ./{fname}-{ai_class}")
    os.system(f"docker build -t {private_repo}/{fname}-{ai_class}:{version} ./{fname}-{ai_class}")
    print("Docker image building completed!!")

    print("Docker image push to Private Repository..")
    os.system(f"docker push {private_repo}/{fname}-{ai_class}:{version}")
    print("Docker image pushing completed!!")

    print(datetime.datetime.now().strftime(
        "%c")[:-4], f"{func}: software upload completed !")

    res = jsonify(
        code="0000",
        message="처리 성공",
    )

    return res


@ app.route('/remove_edgeAi', methods=['POST'])
def remove_edgeAi():
    func = sys._getframe().f_code.co_name
    print(datetime.datetime.now().strftime(
        "%c")[:-4], f"{func}: deleting uploaded Software...")

    json_data = request.get_json(silent=True) # AI ID 만 전달됨 id
    if json_data == None:
        return response.message("0021")

    aid = json_data['aid']

    res = requests.get(f"{SETUP_API_URL}/get_uploadedAiInfo?aid={aid}")
    if res.json()["code"] != "0000":
        return response.message(res.json()["code"])

    filename = res.json()['filename']
    version = res.json()['version']
    ai_class = res.json()['ai_class']
#     fname = filename[:-4]
    fname = filename    # test 에서는 fname = filename

    print(datetime.datetime.now().strftime(
        "%c")[:-4], f"{func}: software ID : {aid} - software name : {fname}")

#     Docker image delete
    print(datetime.datetime.now().strftime(
        "%c")[:-4], f"{func}: docker image {fname}-{ai_class} deleting...")
    os.system(f"docker rmi -f {private_repo}/{fname}-{ai_class}:{version}")
    print(datetime.datetime.now().strftime(
        "%c")[:-4], f"{func}: docker image deleted!!")

    print(datetime.datetime.now().strftime(
        "%c")[:-4], f"{func}: software deleted !")

    return response.message("0000")


@ app.route('/deploy_aiToDevice', methods=['POST'])
def deploy_aiToDevice():
    func = sys._getframe().f_code.co_name
    print(datetime.datetime.now().strftime(
        "%c")[:-4], f" {func}: start deploying software by Kubernetes")

    json_data = request.get_json(silent=True)
    if json_data == None:
        return response.message("0021")

    aid = json_data['aid']  # ai 패키지 ID
### 임시로 ni01 ===  intellivix-worker-01 으로 입력중
    nid = json_data['nid']
#     cid = json_data['cid']  # Cluster ID
#     print(datetime.datetime.now().strftime(
#         "%c")[:-4], f" {func}: kubernetes : deploy software [{sid}] to Cluster [{cid}]....")

    # fname 불러오기
    ai_info_data = requests.get(f"{SETUP_API_URL}/get_uploadedAiInfo?aid={aid}")
    if ai_info_data.json()["code"] != "0000":
        return response.message(ai_info_data.json()["code"])

    filename = ai_info_data.json()['filename']
#     fname = filename[:-4]
    fname = filename.split('-')[0]
    version = ai_info_data.json()['version']
    ai_class = ai_info_data.json()['ai_class']

    print(datetime.datetime.now().strftime(
        "%c")[:-4], f" {func}: software name is {fname}.....")

# POD 생성(yaml 파일이 만들어져있는 상태)
#     os.system(f"kubectl apply -f {fname}-{host_name}.yaml")
    result = subprocess.run(['kubectl', 'apply', '-f', f'{fname}-{ai_class}/{fname}-{ai_class}.yaml'], capture_output=True, text=True)
    print(result.stdout)
    print(result.stderr)

#     # 클러스터명, 디바이스명 불러오기
#     cluster_info_data = requests.get(f"{API_URL}/get_selectedClusterInfo?id={cid}")
#     if cluster_info_data.json()["code"] != "0000":
#         return response.message(cluster_info_data.json()["code"])
#
#     wlist = cluster_info_data.json()['wlist']
#
#     for w in wlist:
#         wid = w['wid']
#         device_info_data = requests.get(f"{API_URL}/get_selectedDeviceInfo?id={wid}")
#         host_name = device_info_data.json()["name"]
#
#         # pod 이 이미 생성되어있으면 지우는 기능
#         command = f"kubectl get pods | grep {fname}-{host_name}"
#         result = subprocess.run(command, shell=True, stdout=subprocess.PIPE, stderr=subprocess.PIPE)
#         check_pod = result.returncode
#
#         if check_pod == 0 :
#             print(datetime.datetime.now().strftime(
#             "%c")[:-4], f" {func}: existing pod deleting....")
#             os.system(f"kubectl delete -f {fname}-{host_name}.yaml")
#             print(datetime.datetime.now().strftime(
#             "%c")[:-4], f" {func}: existing pod deleted....")
#
#         print(datetime.datetime.now().strftime(
#             "%c")[:-4], f" {func}: Making deployment...")
#         deployment = dm.making(fname, host_name, docker_id, version)
#         print(datetime.datetime.now().strftime(
#             "%c")[:-4], f" {func}: ------ deployment ------ ")
#         print(deployment)
#
#         # POD 생성
# #         os.system("kubectl get pod")
#         os.system(f"kubectl apply -f {fname}-{host_name}.yaml")
#         print(datetime.datetime.now().strftime(
#             "%c")[:-4], f" {func}: deploying {fname}-{host_name}.yaml.....")

    print(datetime.datetime.now().strftime(
        "%c")[:-4], f" {func}: deploy completed !")

    return response.message("0000")


@ app.route('/undeploy_aiFromDevice', methods=['POST'])
def undeploy_aiFromDevice():
    func = sys._getframe().f_code.co_name
    print(datetime.datetime.now().strftime(
        "%c")[:-4], f" {func}: start undeploying software by Kubernetes")

    json_data = request.get_json(silent=True)
    if json_data == None:
        return response.message("0021")

    aid = json_data['aid']  # ai 패키지 ID
#     did = json_data['did']  # Device ID
#     print(datetime.datetime.now().strftime(
#         "%c")[:-4], f" {func}: kubernetes : undeploy software [ID : {sid}] to server [ID : {did}]")

    # 디바이스명 불러오기
#     device_info_data = requests.get(f"{SETUP_API_URL}/get_selectedDeviceInfo?id={did}")
#     if res.json()["code"] != "0000":
#         return response.message(res.json()["code"])
#     host_name = device_info_data.json()["name"]

    ai_info_data = requests.get(f"{SETUP_API_URL}/get_uploadedAiInfo?aid={aid}")
    if ai_info_data.json()["code"] != "0000":
        return response.message(ai_info_data.json()["code"])

    filename = ai_info_data.json()['filename']
#     fname = filename[:-4]
    fname = filename
    version = ai_info_data.json()['version']
    ai_class = ai_info_data.json()['ai_class']

#     fileUrl = ai_info_data.json()["fileUrl"]
#     fname = fileURL
    #######################################################
#     print(datetime.datetime.now().strftime(
#         "%c")[:-4], f" {func}: undeploy Software [{fname}] from server [{host_name}]")
    result = subprocess.run(['kubectl', 'delete', '-f', f'{fname}/{fname}-{ai_class}.yaml'], capture_output=True, text=True)
    print(result.stdout)
    print(result.stderr)

    print(datetime.datetime.now().strftime(
        "%c")[:-4], f" {func}: undeploy completed !")

    return response.message("0000")

# DB
# basdir = os.path.abspath(os.path.dirname(__file__))
# dbfile = os.path.join(basdir, 'db.sqlite')
#
# app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///' + dbfile
# app.config['SQLALCHEMY_COMMIT_ON_TEARDOWN'] = True
# app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
# app.config['SECRET_KEY'] = 'jqiowejrojzxcovnklqnweiorjqwoijroi'
#
# db.init_app(app)
# app.app_context().push()
# db.create_all()

if __name__ == '__main__':
    app.run(host='0.0.0.0', threaded=True, port=port)
