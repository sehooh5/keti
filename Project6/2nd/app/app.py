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
import shutil
# docker folder
from docker import getImageTag as git
# k8s folder
from k8s import deployment_maker as dm
from k8s import monitoring_maker as mm
from k8s import node_selector as ns

# sudo 사용으로 k8s config 설정 파일 위치 지정해주기
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

import shutil
# 2.4.3 신규 엣지 클러스터 추가 (add_newCluster 와 연동)
@ app.route('/add_newEdgeCluster', methods=['POST'])
def add_newEdgeCluster():
    func = sys._getframe().f_code.co_name
    print(datetime.datetime.now().strftime(
        "%c")[:-4], f"{func}: new edge cluster making...")

    json_data = request.get_json(silent=True)
    print(datetime.datetime.now().strftime(
        "%c")[:-4], f"{func}: edge json data: {json_data}")
    if json_data == None:
        return response.message("0021")
    mid = json_data['mid']
    wlist = json_data['wlist']

    if mid == None or wlist == None:
        return response.message("0015")

    res = requests.get(f"{API_URL}/get_selectedMasterInfo?id={mid}")
    if res.json()["code"] != "0000":
        return response.message(res.json()["code"])
    mip = res.json()["ip"]
    m_name = res.json()["name"]
    print(datetime.datetime.now().strftime(
        "%c")[:-4], f"{func}: master server ip: {mip}")

    # 마스터 엣지 구성
    m_output = subprocess.check_output(
        f"echo keti | sudo -S kubeadm init --pod-network-cidr=10.244.0.0/16 --apiserver-advertise-address={mip} --node-name {m_name}" , shell=True).decode('utf-8')

    # 마스터 - 워커 연결해주는 명령어
    w_input = m_output.split('root:')[-1].lstrip()
    w_input = w_input.rstrip()

    # 마스터에서 설정해줘야 하는 내용
#     os.system("echo yes | sudo cp -i /etc/kubernetes/admin.conf $HOME/.kube/config")
    os.system("mkdir -p $HOME/.kube")
    os.system("sudo chown $(id -u):$(id -g) $HOME/.kube/config")
    command = ["sudo", "cp", "/etc/kubernetes/admin.conf",  f"/home/{m_name}/.kube/config"]

    # 인터랙티브 덮어쓰기 확인을 자동으로 수락
    try:
        subprocess.run(command, input='y\n', stdout=subprocess.PIPE, stderr=subprocess.PIPE, check=True, universal_newlines=True)
        print("명령어 실행 성공.")
    except subprocess.CalledProcessError as e:
        print(f"오류 발생: {e}")
    os.system("kubectl apply -f https://raw.githubusercontent.com/coreos/flannel/master/Documentation/kube-flannel.yml")


    for w in wlist:
        wid = w["wid"]
        if wid == None:
            return response.message("0015")
        res = requests.get(f"{API_URL}/get_selectedDeviceInfo?id={wid}")

        wip = res.json()["ip"]
        host_name = res.json()["name"]
        host_pwd = "keti"
        print(f"device name : {host_name}, pwd : {host_pwd}")

        # 워커노드와 연결
        w_input = f"sudo {w_input} --node-name {host_name}"
        print(datetime.datetime.now().strftime(
        "%c")[:-4], f"Send a message [{w_input}] to Worker..")
        cli.connect(wip, port=22, username=host_name, password=host_pwd)
        stdin, stdout, stderr = cli.exec_command(w_input, get_pty=True)
        stdin.write('keti\n')
        stdin.flush()
        lines = stdout.readlines()
        print(''.join(lines))
        time.sleep(2.0)
        cli.close()
        print(datetime.datetime.now().strftime(
            "%c")[:-4], f"{func}: worker server ip: {wip}")
        print(
            datetime.datetime.now().strftime(
                "%c")[:-4], f"{func}: connect worker server[{host_name}] with master server!")

    print(datetime.datetime.now().strftime(
        "%c")[:-4], f"{func}: edge clustering completed !")

    return response.message("0000")

# 2.4.4 선택 엣지 클러스터 삭제
## 삭제 시 if 문 사용 안해도되는지 확인 필요
@ app.route('/remove_selectedEdgeCluster', methods=['POST'])
def remove_selectedEdgeCluster():

    func = sys._getframe().f_code.co_name
    print(datetime.datetime.now().strftime(
        "%c")[:-4], f" {func}: deleting edge cluster")

    ips = []
    names = []
    hnames = []
    pwds = []


    json_data = request.get_json(silent=True)
    if json_data == None:
        return response.message("0021")

    # 무선엣지 과제에서는 cluster id만 주어지는데 정보 획득해서 진행
    cid = json_data['id']
    print(datetime.datetime.now().strftime(
        "%c")[:-4], f" {func}: master server ID : {cid}")

    if cid == None:
        return response.message("0015")

    res_cluster = requests.get(f"{API_URL}/get_selectedClusterInfo?id={cid}")
    if res_cluster.json()["code"] != "0000":
        return response.message(res_cluster.json()["code"])
    mid = res_cluster.json()["mid"]
    wlist = res_cluster.json()["wlist"]

    res_master = requests.get(f"{API_URL}/get_selectedMasterInfo?id={mid}")

    ips.append(res_master.json()["ip"])
    names.append(res_master.json()["name"])
    hnames.append(res_master.json()["name"])
    pwds.append("keti")


    for w in wlist:
        # 필요한 정보 얻기
        wid = w["wid"]
        print(datetime.datetime.now().strftime(
            "%c")[:-4], f" {func}: worker ID : {wid}")
        if wid == None:
            return response.message("0015")
        res_device = requests.get(f"{API_URL}/get_selectedDeviceInfo?id={wid}")

        ips.append(res_device.json()["ip"])
        names.append(res_device.json()["name"])
        hnames.append(res_device.json()["name"])
        pwds.append("keti")

#     ips.append("192.168.0.14")
#     names.append("edge-master-01")
#     hnames.append('edge-master-01')
#     pwds.append("keti")
#     ips.append("192.168.0.9")
#     names.append("edge-worker-01")
#     hnames.append('edge-worker-01')
#     pwds.append("keti")

    for ip, name, hname, pwd in zip(ips, names, hnames, pwds):
        print(datetime.datetime.now().strftime(
        "%c")[:-4],f"{name} : delete node from cluster!")
        os.system(f"kubectl delete node {name}")

        if "master" in  hname: # host_name에 master 라는 단어가 있을 시에 삭제/// if문 안써도되는지 확인해보기
            cli.connect(ip, port=22, username=hname, password=pwd)
            stdin, stdout, stderr = cli.exec_command(
                "echo y | sudo kubeadm reset", get_pty=True)
            stdin.write('keti\n')
            stdin.flush()

            lines = stdout.readlines()
            print(''.join(lines))

            time.sleep(2.0)
            cli.close()
        else :
            print(datetime.datetime.now().strftime(
            "%c")[:-4],f"SSH Connect to {name}")

            print(f"IP : {ip} / username : {hname} / password : {pwd}")
            cli.connect(ip, port=22, username=hname, password=pwd)

            print(datetime.datetime.now().strftime(
            "%c")[:-4],f"{name} : kubeadm reset!")
            stdin, stdout, stderr = cli.exec_command(
                "echo y | sudo kubeadm reset", get_pty=True)
            stdin.write('keti\n')
            stdin.flush()

            lines = stdout.readlines()
            print(''.join(lines))

            time.sleep(2.0)
            cli.close()

    print(datetime.datetime.now().strftime(
        "%c")[:-4], f" {func}: edge cluster deleted!!!")

    return response.message("0000")


# 2.5.3 신규 엣지 AI 패키지 추가 인터페이스 & # 2.5.5 선택 엣지 AI 패키지의 정보 수정 인터페이스
@ app.route('/upload_edgeAi', methods=['POST'])
def upload_edgeAi():
    func = sys._getframe().f_code.co_name
    print(datetime.datetime.now().strftime(
        "%c")[:-4], f"{func}: start uploading a new software")
    json_data = request.get_json(silent=True)

    if json_data == None:
        return response.message("0021")

    filename = json_data['filename']
    version = json_data['version']

    fname = filename[:-4]
    print(datetime.datetime.now().strftime(
    "%c")[:-4], f"{func}: software name: {fname}")

    # AI의 이전 버전 있으면 삭제하는 부분
    tag_list = git.get_image_tags(docker_id, fname) # docker tag list
    if len(tag_list) >= 1:
        for tag in tag_list:
            os.system(f"docker rmi -f {docker_id}/{fname}:{tag}")


#     print(f"{file_path}/{filename} : 에 있는 파일  풀기 시작")
#     zip_ref = zipfile.ZipFile(f"{file_path}/{filename}")
#     print('추출')
#     zip_ref.extractall()
#     print('종료')
#     zip_ref.close()

    # ZIP 파일 압축풀기
    zip_file_path = f"{file_path}/{filename}"
    try:
        # Zip 파일 열기
        with zipfile.ZipFile(zip_file_path, 'r') as zip_ref:
            # 압축 해제
            zip_ref.extractall('monitoring')
        print(f"Zip file '{zip_file_path}' successfully extracted to '/monitoring'.")
    except zipfile.BadZipFile as e:
        print(f"Error: {zip_file_path} is not a valid zip file. {e}")
    except Exception as e:
        print(f"Error extracting zip file: {e}")

    print(datetime.datetime.now().strftime("%c")[:-4], f"{func}: docker image building...")
    print(f"명령어확인 ----- docker build -f {fname}/Dockerfile -t sehooh5/{fname}:{version} .")
    os.system(
        f"docker build -f {fname}/Dockerfile -t sehooh5/{fname}:{version} .")
    print("Docker image building completed!!")

    print("Docker image push to Docker hub..")
    os.system(f"docker push sehooh5/{fname}:{version}")
    print("Docker image pushing completed!!")


    print(datetime.datetime.now().strftime(
        "%c")[:-4], f"{func}: software upload completed !")

    res = jsonify(
        code="0000",
        message="처리 성공",
    )

#     # 압축 해제된 폴더 지우기
#     try:
#         shutil.rmtree(fname)
#         print(f"Directory '{fname}' deleted successfully.")
#     except OSError as e:
#         print(f"Error deleting directory '{fname}': {e}")

    return res

# 2.5.4 선택 엣지 AI 삭제 인터페이스
@ app.route('/remove_uploadedEdgeAi', methods=['POST'])
def remove_uploadedEdgeAi():
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
    print(res.json())
    # json 응답으로부터 fname 추출
#     fileUrl = res.json()["fileUrl"]
#     filename = fileUrl.split('/')[-1]
#     if fileUrl.find("zip") != -1:
#         fname = filename.split('.')[0]

    filename = res.json()['name']
    version = res.json()['version']
    fname = filename[:-4]

    print(datetime.datetime.now().strftime(
        "%c")[:-4], f"{func}: software ID : {id} - software name : {fname}")

    # Docker image delete
    print(datetime.datetime.now().strftime(
        "%c")[:-4], f"{func}: docker image {fname} deleting...")
    os.system(f"docker rmi -f sehooh5/{fname}:{version}")
    print(datetime.datetime.now().strftime(
        "%c")[:-4], f"{func}: docker image deleted!!")

    print(datetime.datetime.now().strftime(
        "%c")[:-4], f"{func}: software deleted !")

    return response.message("0000")


## 두 방법 다 진행해야함
# 2.6.1 클러스터 기반 엣지 AI 패키지 배포 인터페이스
@ app.route('/deploy_aiToCluster', methods=['POST'])
def deploy_aiToCluster():
    func = sys._getframe().f_code.co_name
    print(datetime.datetime.now().strftime(
        "%c")[:-4], f" {func}: start deploying software by Kubernetes")

    docker_id = "sehooh5"

    json_data = request.get_json(silent=True)
    if json_data == None:
        return response.message("0021")


    sid = json_data['sid']  # ai 패키지 ID
    cid = json_data['cid']  # Cluster ID
    print(datetime.datetime.now().strftime(
        "%c")[:-4], f" {func}: kubernetes : deploy software [{sid}] to Cluster [{cid}]....")

    # fname 불러오기
    ai_info_data = requests.get(f"{API_URL}/get_selectedEdgeAiInfo?id={sid}")
    if ai_info_data.json()["code"] != "0000":
        return response.message(ai_info_data.json()["code"])

    filename = ai_info_data.json()['name']
    fname = filename[:-4]
    version = ai_info_data.json()['version']

    print(datetime.datetime.now().strftime(
        "%c")[:-4], f" {func}: software name is {fname}.....")

    # 클러스터명, 디바이스명 불러오기
    cluster_info_data = requests.get(f"{API_URL}/get_selectedClusterInfo?id={cid}")
    if cluster_info_data.json()["code"] != "0000":
        return response.message(cluster_info_data.json()["code"])

    wlist = cluster_info_data.json()['wlist']

    for w in wlist:
        wid = w['wid']
        device_info_data = requests.get(f"{API_URL}/get_selectedDeviceInfo?id={wid}")
        host_name = device_info_data.json()["name"]

        # pod 이 이미 생성되어있으면 지우는 기능
        command = f"kubectl get pods | grep {fname}-{host_name}"
        result = subprocess.run(command, shell=True, stdout=subprocess.PIPE, stderr=subprocess.PIPE)
        check_pod = result.returncode

        if check_pod == 0 :
            print(datetime.datetime.now().strftime(
            "%c")[:-4], f" {func}: existing pod deleting....")
            os.system(f"kubectl delete -f {fname}-{host_name}.yaml")
            print(datetime.datetime.now().strftime(
            "%c")[:-4], f" {func}: existing pod deleted....")

        print(datetime.datetime.now().strftime(
            "%c")[:-4], f" {func}: Making deployment...")
        deployment = dm.making(fname, host_name, docker_id, version)
        print(datetime.datetime.now().strftime(
            "%c")[:-4], f" {func}: ------ deployment ------ ")
        print(deployment)

        # POD 생성
#         os.system("kubectl get pod")
        os.system(f"kubectl apply -f {fname}-{host_name}.yaml")
        print(datetime.datetime.now().strftime(
            "%c")[:-4], f" {func}: deploying {fname}-{host_name}.yaml.....")

    print(datetime.datetime.now().strftime(
        "%c")[:-4], f" {func}: deploy completed !")

    return response.message("0000")

# 2.6.2. 단말 기반 엣지 AI 패키지 배포 인터페이스
@ app.route('/deploy_aiToDevice', methods=['POST'])
def deploy_aiToDevice():
    func = sys._getframe().f_code.co_name
    print(datetime.datetime.now().strftime(
        "%c")[:-4], f" {func}: start deploying software by Kubernetes")

    docker_id = "sehooh5"

    json_data = request.get_json(silent=True)
    if json_data == None:
        return response.message("0021")

    sid = json_data['sid']  # ai 패키지 ID
    did = json_data['did']  # Device ID
    print(datetime.datetime.now().strftime(
        "%c")[:-4], f" {func}: kubernetes : deploy software [{sid}] to Device [{did}]....")

    # fname 불러오기
    ai_info_data = requests.get(f"{API_URL}/get_selectedEdgeAiInfo?id={sid}")
    if ai_info_data.json()["code"] != "0000":
        return response.message(ai_info_data.json()["code"])

    filename = ai_info_data.json()['name']
    fname = filename[:-4]
    version = ai_info_data.json()['version']

    print(datetime.datetime.now().strftime(
        "%c")[:-4], f" {func}: software name is {fname}.....")

    # 디바이스명 불러오기
    device_info_data = requests.get(f"{API_URL}/get_selectedDeviceInfo?id={did}")
    host_name = device_info_data.json()["name"]

    # pod 이 이미 생성되어있으면 지우는 기능
    command = f"kubectl get pods | grep {fname}-{host_name}"
    result = subprocess.run(command, shell=True, stdout=subprocess.PIPE, stderr=subprocess.PIPE)
    check_pod = result.returncode

    if check_pod == 0 :
        print(datetime.datetime.now().strftime(
        "%c")[:-4], f" {func}: existing pod deleting....")
        os.system(f"kubectl delete -f {fname}-{host_name}.yaml")
        print(datetime.datetime.now().strftime(
        "%c")[:-4], f" {func}: existing pod deleted....")

    print(datetime.datetime.now().strftime(
        "%c")[:-4], f" {func}: Making deployment...")
    deployment = dm.making(fname, host_name, docker_id, version)
    print(datetime.datetime.now().strftime(
        "%c")[:-4], f" {func}: ------ deployment ------ ")
    print(deployment)

    # POD 생성
    os.system(f"kubectl apply -f {fname}-{host_name}.yaml")
    print(datetime.datetime.now().strftime(
        "%c")[:-4], f" {func}: deploying {fname}-{host_name}.yaml.....")

    print(datetime.datetime.now().strftime(
        "%c")[:-4], f" {func}: deploy completed !")

    return response.message("0000")

# 2.6.2-2 단말 기반 엣지 AI 패키지 삭제 인터페이스 (추가해야할 듯)
@ app.route('/remove_deploySwInfo', methods=['POST'])
def remove_deploySwInfo():
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


# 2.13 마스터 서버의 사용 가능한 서비스 포트 조회
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


# 2.14 마스터 서버의 사용 가능한 타깃 포트 조회
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


# 2.15 마스터 서버의 사용 가능한 노드 포트 조회
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
app.app_context().push()
# db.app = app
db.create_all()

if __name__ == '__main__':
    app.run(host='0.0.0.0', threaded=True, port=port)
