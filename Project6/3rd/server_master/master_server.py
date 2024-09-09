#!/usr/bin/env python
## app.py 기반 master 에서 실행되는 서버
from importlib import import_module
from typing import List
from flask import Flask, render_template, Response, request, jsonify
from flask_cors import CORS, cross_origin
import json
import requests
import os
from models import db, SW_up, Server, Server_SW
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

os.environ['KUBECONFIG'] = '/home/edge-master-01/.kube/config'

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


API_URL = "http://123.214.186.244:4880"
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

    if json_data == None:
        return response.message("0015")

    aid = json_data['aid']
    filename = json_data['filename']
    version = json_data['version']
    ai_class = json_data['ai_class'] # 추가

#     fname = filename[:-4]
    fname = filename    # test 에서는 fname = filename
    print(datetime.datetime.now().strftime(
    "%c")[:-4], f"{func}: software name: {fname}")

    print(datetime.datetime.now().strftime("%c")[:-4], f"{func}: docker image building...")
    print(f"명령어확인 ----- docker build -f {fname}/Dockerfile -t {private_repo}/{fname}-{ai_class}:{version} .")
    os.system(
        f"docker build -f {fname}/Dockerfile -t {private_repo}/{fname}-{ai_class}:{version} .")
    print("Docker image building completed!!")

    print("Docker image push to Docker hub..")
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

    id = json_data['id']

    res = requests.get(f"{API_URL}/get_selectedEdgeAiInfo?id={id}")
    if res.json()["code"] != "0000":
        return response.message(res.json()["code"])

    filename = res.json()['name']
    version = res.json()['version']
    ai_class = res.json()['ai_class']
#     fname = filename[:-4]
    fname = filename    # test 에서는 fname = filename

    print(datetime.datetime.now().strftime(
        "%c")[:-4], f"{func}: software ID : {id} - software name : {fname}")

    # Docker image delete
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
#     cid = json_data['cid']  # Cluster ID
#     print(datetime.datetime.now().strftime(
#         "%c")[:-4], f" {func}: kubernetes : deploy software [{sid}] to Cluster [{cid}]....")

    # fname 불러오기
    ai_info_data = requests.get(f"{API_URL}/get_selectedEdgeAiInfo?id={aid}")
    if ai_info_data.json()["code"] != "0000":
        return response.message(ai_info_data.json()["code"])

    filename = ai_info_data.json()['name']
#     fname = filename[:-4]
    fname = filename
    version = ai_info_data.json()['version']
    ai_class = ai_info_data.json()['ai_class']

    print(datetime.datetime.now().strftime(
        "%c")[:-4], f" {func}: software name is {fname}.....")

# POD 생성(yaml 파일이 만들어져있는 상태)
#     os.system(f"kubectl apply -f {fname}-{host_name}.yaml")
    os.system(f"kubectl apply -f {fname}-{ai_class}.yaml")


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

    sid = json_data['sid']  # ai 패키지 ID
    did = json_data['did']  # Device ID
    print(datetime.datetime.now().strftime(
        "%c")[:-4], f" {func}: kubernetes : undeploy software [ID : {sid}] to server [ID : {did}]")

    # 디바이스명 불러오기
    device_info_data = requests.get(f"{API_URL}/get_selectedDeviceInfo?id={did}")
    if res.json()["code"] != "0000":
        return response.message(res.json()["code"])
    host_name = device_info_data.json()["name"]

    # fname 불러오기
    ai_info_data = requests.get(f"{API_URL}/get_selectedEdgeAiInfo?id={sid}")
    if ai_info_data.json()["code"] != "0000":
        return response.message(ai_info_data.json()["code"])

    filename = ai_info_data.json()['name']
    fname = filename[:-4]
    #### url에서 filename 만 추출해서 진행해야함!!!!!!!! ####

#     fileUrl = ai_info_data.json()["fileUrl"]
#     fname = fileURL
    #######################################################
    print(datetime.datetime.now().strftime(
        "%c")[:-4], f" {func}: undeploy Software [{fname}] from server [{host_name}]")

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
