#!/usr/bin/env python
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
# k8s folder
from k8s import deployment_maker as dm
from k8s import monitoring_maker as mm
from k8s import node_selector as ns

app = Flask(__name__)
app.config['JSON_AS_ASCII'] = False  # jsonify 한글깨짐 해결
CORS(app)

# 다른 서버에 명령 보낼때 사용
cli = paramiko.SSHClient()
cli.set_missing_host_key_policy(paramiko.AutoAddPolicy)

# 랜덤한 문자열 생성기
_LENGTH = 4
string_pool = string.ascii_letters + string.digits


def sid_maker():
    sid = ""
    for i in range(_LENGTH):
        sid += random.choice(string_pool)
    return sid


# 포트번호 생성
def port_maker(len):
    port = ""
    for i in range(len):
        port += random.choice(string.digits)
    return port


def node_port():
    num = str(random.randint(0000, 2766))
    if len(num) == 3:
        print("nope", f"0{num}")
        num = f"30{num}"
    elif len(num) == 2:
        num = f"300{num}"
    elif len(num) == 1:
        num = f"3000{num}"
    else:
        num = f"3{num}"
    return num


API_URL = "http://123.214.186.244:9997"

# IP 주소
ips = subprocess.check_output("hostname -I", shell=True).decode('utf-8')
ip = ips.split(' ')[0]
port = "5432"

# os.environ['OPEN_WINDOW'] = "NO"


@ app.route('/')
def index():
    

    return render_template('index.html', list=datas)


# 1 마스터 서버에 업로드한 신규 소프트웨어 등록
@ app.route('/add_newUploadSw', methods=['POST'])
def add_newUploadSw():
    func = sys._getframe().f_code.co_name
    print(datetime.datetime.now().strftime(
        "%c")[:-4], f"{func}: start uploading a new software")
    json_data = request.get_json(silent=True)

    if json_data == None:
        return response.message("0021")

    name = json_data['name']
    # 최적환경
    # 포트번호 - 근데 이건 배포할때 필요함
    copyright = json_data['copyright']
    type = json_data['type'] # 기능
    desc = json_data['description']
    filename = json_data['file']
    sid = json_data['sid']
    # VMS 서버로부터 마스터서버로 파일 다운로드
    if filename.find("zip") != -1:
        fname = filename[:-4]
        if "_" in fname:
            fname = fname.replace("_", "-")

        print(datetime.datetime.now().strftime(
            "%c")[:-4], f"{func}: software name: {fname}")
        with open(f"{fname}.zip", 'wb') as select_cam:
            data = requests.get(f"{API_URL}/download?filename={filename}")
            select_cam.write(data.content)
        # print("select_cam : ", select_cam)

        zip_ref = zipfile.ZipFile(f"{fname}.zip")
        zip_ref.extractall(fname)
        zip_ref.close()
        print(datetime.datetime.now().strftime(
            "%c")[:-4], f"{func}: [{fname}] file uploading completed !")
        print(datetime.datetime.now().strftime(
            "%c")[:-4], f"{func}: docker image building...")
        print(f"명령어확인 ----- docker build -f {fname}/{fname} -t sehooh5/{fname}:latest .")
        os.system(
            f"docker build -f {fname}/{fname} -t sehooh5/{fname}:latest .")
        print("Docker image building completed!!")
        # docker login status 확인
        try:
            print("Docker login status is Checking...")
            subprocess.check_output("docker info | grep Username", shell=True).decode('utf-8')
        except subprocess.CalledProcessError:
            print("Docker login status : none")
            # docker login 실행
            print("Docker login..")
            os.system("docker login -u sehooh5 -p @Dhtpgh1234")
        print("Docker image push to Docker hub..")
        os.system(f"docker push sehooh5/{fname}:latest")
        print("Docker image pushing completed!!")
    # elif filename.find("prometheus"):
    #     with open(filename, 'wb') as filename:
    #         data = requests.get(f"{API_URL}/download?filename={filename}")
    #         filename.write(data.content)
    else:
        fname = filename
        print(datetime.datetime.now().strftime(
            "%c")[:-4], f"{func}: software name: {fname}")
        with open(filename, 'wb') as file:
            data = requests.get(f"{API_URL}/download?filename={filename}")
            file.write(data.content)



    # 2. software_up 테이블에 데이터 저장
    sw = SW_up(sid=sid, name=name, fname=fname,
               copyright=copyright, type=type, description=desc)
    db.session.add(sw)
    db.session.commit

    print(datetime.datetime.now().strftime(
        "%c")[:-4], f"{func}: software upload completed !")

    res = jsonify(
        code="0000",
        message="처리 성공",
        sid=sid
    )
    return res


# 2 마스터 서버에 업로드된 SW 삭제
@ app.route('/remove_uploadSw', methods=['POST'])
def remove_uploadSw():
    func = sys._getframe().f_code.co_name
    print(datetime.datetime.now().strftime(
        "%c")[:-4], f"{func}: deleting uploaded Software...")

    json_data = request.get_json(silent=True)
    if json_data == None:
        return response.message("0021")

    sid = json_data['sid']

    fname = db.session.query(SW_up.fname).filter(SW_up.sid == sid).first()[0]
    print(datetime.datetime.now().strftime(
        "%c")[:-4], f"{func}: software ID : {sid} - software name : {fname}")

    # Docker image delete
    print(datetime.datetime.now().strftime(
        "%c")[:-4], f"{func}: docker image {fname} deleting...")
    os.system(f"docker rmi -f sehooh5/{fname}")
    print(datetime.datetime.now().strftime(
        "%c")[:-4], f"{func}: docker image deleted!!")

    sw = db.session.query(SW_up).filter(SW_up.sid == sid).first()

    db.session.delete(sw)
    db.session.commit()
    print(datetime.datetime.now().strftime(
        "%c")[:-4], f"{func}: software deleted !")

    return response.message("0000")


# 3 워커 서버에 AI 배포
@ app.route('/add_newDeploySwInfo', methods=['POST'])
def add_newDeploySwInfo():
    func = sys._getframe().f_code.co_name
    print(datetime.datetime.now().strftime(
        "%c")[:-4], f" {func}: start deploying software by Kubernetes")

    json_data = request.get_json(silent=True)
    if json_data == None:
        return response.message("0021")
    wid = json_data['wid']  # SW ID
    sid = json_data['sid']  # Server ID
    print(datetime.datetime.now().strftime(
        "%c")[:-4], f" {func}: kubernetes : deploy software [{wid}] to edge Server [{sid}]....")
    # 노드명 불러오기
    res = requests.get(f"{API_URL}/get_edgeInfo?id={sid}")
    if res.json()["code"] != "0000":
        return response.message(res.json()["code"])
    node_name = res.json()["name"]
    target_port = json_data['targetport']  # AI 등록 시 입력하는 port 번호
    port = f"6{port_maker(3)}" # 중복 확인 안하고 그냥 생성
    node_port = node_port() # 중복 확인 안하고 그냥 생성


    # fname 불러오기
    fname = db.session.query(SW_up.fname).filter(SW_up.sid == wid).first()[0]
    if "_" in fname:
        fname = fname.replace("_", "-")
    print(datetime.datetime.now().strftime(
        "%c")[:-4], f" {func}: software name is {fname}.....")

    docker_id = "sehooh5"
    print(datetime.datetime.now().strftime(
        "%c")[:-4], f" {func}: Making deployment...")
    deployment = dm.making(fname, port, target_port,
                           node_port, node_name, docker_id)
    print(datetime.datetime.now().strftime(
        "%c")[:-4], f" {func}: ------ deployment ------ ")
    print(deployment)

    os.system(f"kubectl apply -f {fname}-{node_name}.yaml")
    print(datetime.datetime.now().strftime(
        "%c")[:-4], f" {func}: deploying {fname}-{node_name}.yaml.....")

    s = Server_SW(sid=sid, wid=wid, serviceport=port,
                  nodeport=node_port, targetport=target_port)
    db.session.add(s)
    db.session.commit()
    print(datetime.datetime.now().strftime(
        "%c")[:-4], f" {func}: deploy completed !")

    return response.message("0000")


# 4 마스터/워커 서버에 배포된 SW 삭제
@ app.route('/remove_deploySwInfo', methods=['POST'])
def remove_deploySwInfo():
    func = sys._getframe().f_code.co_name
    print(datetime.datetime.now().strftime(
        "%c")[:-4], f" {func}: start undeploying software by Kubernetes")

    json_data = request.get_json(silent=True)
    if json_data == None:
        return response.message("0021")
    wid = json_data['wid']
    sid = json_data['sid']
    print(datetime.datetime.now().strftime(
        "%c")[:-4], f" {func}: kubernetes : undeploy software [ID : {wid}] to server [ID : {sid}]")

    # 노드명 불러오기
    res = requests.get(f"{API_URL}/get_edgeInfo?id={sid}")
    if res.json()["code"] != "0000":
        return response.message(res.json()["code"])
    node_name = res.json()["name"]

    # fname 불러오기
    fname = db.session.query(SW_up.fname).filter(SW_up.sid == wid).first()[0]
    print(datetime.datetime.now().strftime(
        "%c")[:-4], f" {func}: undeploy Software [{fname}] from server [{node_name}]")
    if fname.find("prometheus") == 0:
        os.system(f"kubectl delete -f {fname}")
    os.system(f"kubectl delete -f {fname}-{node_name}.yaml")

    sw = db.session.query(Server_SW).filter(
        Server_SW.sid == sid, Server_SW.wid == wid).first()
    db.session.delete(sw)
    db.session.commit()
    print(datetime.datetime.now().strftime(
        "%c")[:-4], f" {func}: undeploy completed !")

    return response.message("0000")


# 5 마스터 서버의 사용 가능한 서비스 포트 조회
@ app.route('/get_servicePort', methods=['POST'])
def get_servicePort():
    func = sys._getframe().f_code.co_name
    print(datetime.datetime.now().strftime(
        "%c")[:-4], f" {func}: start")

    json_data = request.get_json(silent=True)
    if json_data == None:
        return response.message("0021")

    cid = json_data['cid']
    # 노드명 불러오기
    res = requests.get(f"{API_URL}/get_edgeClusterInfo?cid={cid}")
    if res.json()["code"] != "0000":
        return response.message(res.json()["code"])
    sid = res.json()["mid"]

    p_list = db.session.query(Server_SW.serviceport).filter(
        Server_SW.sid == sid).all()
    port_list = []
    for p in p_list:
        port = p[0]
        port_list.append(port)

    port = f"6{port_maker(3)}"
    while True:
        if port in port_list:
            port = f"6{port_maker(3)}"
            print(datetime.datetime.now().strftime(
                "%c")[:-4], f" {func}: port is already used. re-making port : {port}")
        else:
            print(f"service port : {port}")
            break

    res = jsonify(
        code="0000",
        message="처리 성공",
        port=port
    )
    return res


# 6 마스터 서버의 사용 가능한 타깃 포트 조회
@ app.route('/get_targetPort', methods=['POST'])
def get_targetPort():
    func = sys._getframe().f_code.co_name
    print(datetime.datetime.now().strftime(
        "%c")[:-4], f" {func}: start")

    json_data = request.get_json(silent=True)
    if json_data == None:
        return response.message("0021")

    cid = json_data['cid']
    # 노드명 불러오기
    res = requests.get(f"{API_URL}/get_edgeClusterInfo?cid={cid}")
    if res.json()["code"] != "0000":
        return response.message(res.json()["code"])
    sid = res.json()["mid"]

    p_list = db.session.query(Server_SW.targetport).filter(
        Server_SW.sid == sid).all()
    port_list = []
    for p in p_list:
        port = p[0]
        port_list.append(port)

    port = f"5{port_maker(3)}"
    while True:
        if port in port_list:
            port = f"5{port_maker(3)}"
            print(datetime.datetime.now().strftime(
                "%c")[:-4], f" {func}: port is already used. re-making port : {port}")
        else:
            print(datetime.datetime.now().strftime(
                "%c")[:-4], f" {func}: target port : {port}")
            break

    res = jsonify(
        code="0000",
        message="처리 성공",
        port=port
    )
    return res


# 7 마스터 서버의 사용 가능한 노드 포트 조회
@ app.route('/get_nodePort', methods=['POST'])
def get_nodePort():
    func = sys._getframe().f_code.co_name
    print(datetime.datetime.now().strftime(
        "%c")[:-4], f" {func}: start")

    json_data = request.get_json(silent=True)
    if json_data == None:
        return response.message("0021")

    cid = json_data['cid']
    # 노드명 불러오기
    res = requests.get(f"{API_URL}/get_edgeClusterInfo?cid={cid}")
    if res.json()["code"] != "0000":
        return response.message(res.json()["code"])
    sid = res.json()["mid"]

    p_list = db.session.query(Server_SW.nodeport).filter(
        Server_SW.sid == sid).all()
    port_list = []
    for p in p_list:
        port = p[0]
        port_list.append(port)

    port = node_port()

    while True:
        if port in port_list:
            port = node_port()
            print(datetime.datetime.now().strftime(
                "%c")[:-4], f" {func}: port is already used. re-making port : {port}")
        else:
            print(datetime.datetime.now().strftime(
                "%c")[:-4], f" {func}: node port : {port}")
            break

    res = jsonify(
        code="0000",
        message="처리 성공",
        port=port
    )
    return res


# DB관련
# 현재있는 파일의 디렉토리 절대경로
basdir = os.path.abspath(os.path.dirname(__file__))
# basdir 경로안에 DB파일 만들기
dbfile = os.path.join(basdir, 'db.sqlite')

# SQLAlchemy 설정

# 내가 사용 할 DB URI
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///' + dbfile
# 비지니스 로직이 끝날때 Commit 실행(DB반영)
app.config['SQLALCHEMY_COMMIT_ON_TEARDOWN'] = True
# 수정사항에 대한 TRACK
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
# SECRET_KEY
app.config['SECRET_KEY'] = 'jqiowejrojzxcovnklqnweiorjqwoijroi'

db.init_app(app)
db.app = app
db.create_all()

if __name__ == '__main__':
    app.run(host='0.0.0.0', threaded=True, port=port)
