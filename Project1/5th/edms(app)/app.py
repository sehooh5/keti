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


API_URL = "http://123.214.186.244:4882"

# IP 주소
ips = subprocess.check_output("hostname -I", shell=True).decode('utf-8')
ip = ips.split(' ')[0]
port = "5000"

@ app.route('/')
def index():
    # 해당 컴퓨터의 worker node 들 이름 가져오기 - names 에 저장
    nodes = subprocess.check_output(
        "kubectl get node", shell=True).decode('utf-8')

    nodes_split = nodes.split('\n')
    len_nodes = len(nodes_split)-1

    name_list = nodes_split[1:len_nodes]
    names = []
    for name in name_list:
        name = name.split(' ')[0]
        if name.find('master') == -1:
            names.append(name)

    # 해당 노드이름으로 노드ID 를 찾고, select-cam 의 nodeport 조회
    datas = []
    res = requests.get(f"{API_URL}/get_edgeList")
    list = res.json()['list']
    for n in list:
        if n.get('name') in names:
            nodename = n.get('name')
            eid = n.get('id')
            wids = db.session.query(Server_SW.wid).filter(
                eid == Server_SW.sid).all()
            for wid in wids:
                fname = db.session.query(SW_up.fname).filter(
                    SW_up.sid == wid[0]).first()[0]
                if fname == "select-cam":
                    sw_id = wid[0]

            nodeport = db.session.query(Server_SW.nodeport).filter(
                Server_SW.sid == eid, Server_SW.wid == sw_id).first()[0]
            data = {"nodename": nodename, "nodeport": nodeport}
            datas.append(data)

    print("전송 데이터 : ", datas)

    return render_template('index.html', list=datas)


# 2.1 신규 엣지 클러스터 추가 (get_edgeInfo 사용)
@ app.route('/add_newEdgeCluster', methods=['POST'])
def add_newEdgeCluster():
    func = sys._getframe().f_code.co_name
    print(datetime.datetime.now().strftime("%c")[:-4], f"{func}: new edge cluster making...")

    json_data = request.get_json(silent=True)
    print(datetime.datetime.now().strftime(
        "%c")[:-4], f"{func}: edge json data: {json_data}")
    if json_data == None:
        return response.message("0021")
    mid = json_data['mid']
    wlist = json_data['wlist']

    if mid == None or wlist == None:
        return response.message("0015")

    res = requests.get(f"{API_URL}/get_edgeInfo?id={mid}")
    print(res.json())
    if res.json()["code"] != "0000":
        return response.message(res.json()["code"])
    mip = res.json()["ip"]
    print(datetime.datetime.now().strftime(
        "%c")[:-4], f"{func}: master server ip: {mip}")

    # 마스터 엣지 구성
    m_output = subprocess.check_output(
        f"echo keti | sudo -S kubeadm init --pod-network-cidr=10.244.0.0/16 --apiserver-advertise-address={mip}", shell=True).decode('utf-8')
    # 마스터 - 워커 연결해주는 명령어
    w_input = m_output.split('root:')[-1].lstrip()
    w_input = f"sudo {w_input}"

#     # 환경 변수를 명시적으로 전달
#     home_dir = os.path.expanduser("~")

#     try:
#         # ~/.kube 디렉토리가 없으면 생성
#         subprocess.run(['mkdir', '-p', f"{home_dir}/.kube"], check=True)
#
#         # admin.conf 파일 복사
#         subprocess.run(['sudo', 'cp', '/etc/kubernetes/admin.conf', f"{home_dir}/.kube/config"], check=True)
#
#         # 파일 소유권 변경
#         subprocess.run(['sudo', 'chown', f"{os.getuid()}:{os.getgid()}", f"{home_dir}/.kube/config"], check=True)
#
#         print("Command executed successfully")
#     except subprocess.CalledProcessError as e:
#         print(f"An error occurred: {e}")

#     # 마스터에서 설정해줘야 하는 내용
#     os.system("mkdir -p $HOME/.kube")
#     os.system("sudo chown $(id -u):$(id -g) $HOME/.kube/config")
#     command = ["sudo", "cp", "/etc/kubernetes/admin.conf",  "$(echo $HOME)/.kube/config"]
#     # 인터랙티브 덮어쓰기 확인을 자동으로 수락
#     try:
#         subprocess.run(command, input='y\n', stdout=subprocess.PIPE, stderr=subprocess.PIPE, check=True, universal_newlines=True)
#         print("명령어 실행 성공.")
#     except subprocess.CalledProcessError as e:
#         print(f"오류 발생: {e}")

#     os.system("mkdir -p $HOME/.kube")
#     time.sleep(1.0)
#
#     cp_command = f'yes | sudo cp /etc/kubernetes/admin.conf $HOME/.kube/config'
#     subprocess.run(cp_command, shell=True, check=True)
#     time.sleep(1.0)
#
#     chown_command = f'sudo chown $(id -u):$(id -g) $HOME/.kube/config'
#     subprocess.run(chown_command, shell=True, check=True)
#     time.sleep(1.0)
#
#     os.system("kubectl apply -f https://raw.githubusercontent.com/coreos/flannel/master/Documentation/kube-flannel.yml")
#     time.sleep(1.0)

### 7/8 이거로 해보기 (무선엣지)
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
        res = requests.get(f"{API_URL}/get_edgeInfo?id={wid}")

        wip = res.json()["ip"]
        host_name = res.json()["host_name"]
        host_pwd = res.json()["host_pwd"]

        # 워커노드와 연결
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


# 2.2 엣지 서버 이름 조회 인터페이스
@ app.route('/get_edgeName', methods=['GET'])
def get_edgeName():
    func = sys._getframe().f_code.co_name
    print(datetime.datetime.now().strftime(
        "%c")[:-4], f"{func}: start")

    nodes = subprocess.check_output(
        "kubectl get node", shell=True).decode('utf-8')

    nodes_split = nodes.split('\n')
    len_nodes = len(nodes_split)-1

    name_list = nodes_split[1:len_nodes]
    names = []
    for name in name_list:
        n = {"name": name.split(' ')[0]}
        names.append(n)

    print(datetime.datetime.now().strftime(
        "%c")[:-4], f"{func}: edge name list: {names}")
    print(datetime.datetime.now().strftime(
        "%c")[:-4], f"{func}: end")

    res = jsonify(
        code="0000",
        message="처리 성공",
        nlist=names
    )
    return res


# 2.3 엣지서버에 디바이스 연결
@ app.route('/connect_device', methods=['POST'])
def connect_device():
    func = sys._getframe().f_code.co_name
    print(datetime.datetime.now().strftime(
        "%c")[:-4], f"{func}: start")

    json_data = request.get_json(silent=True)
    if json_data == None:
        return response.message("0021")

    eid = json_data['eid']
    did = json_data['did']
    print(eid,did)

    device = requests.get(f"{API_URL}/get_deviceInfo?id={did}")
    device_name = device.json()["name"]

    edge = requests.get(f"{API_URL}/get_edgeInfo?id={eid}")
    edge_name = edge.json()["name"]
    edge_ip = edge.json()["ip"]

    print(
        datetime.datetime.now().strftime(
            "%c")[:-4], f"{func}: connect Server [{edge_name}] with device [{device_name}]....")

    # 노드포트 찾기위한 과정
    wids = db.session.query(Server_SW.wid).filter(eid == Server_SW.sid).all()
    for wid in wids:
        fname = db.session.query(SW_up.fname).filter(
            SW_up.sid == wid[0]).first()[0]
        if fname == "select-cam":
            sw_id = wid[0]

    nodeport = db.session.query(Server_SW.nodeport).filter(
        Server_SW.sid == eid, Server_SW.wid == sw_id).first()[0]
    print(datetime.datetime.now().strftime(
        "%c")[:-4], f"{func}: using nodeport: {nodeport}")

    # 디바이스 정보 추출
    d_url = "rtsp://root:keti@" + \
        device.json()["ip"]+"/onvif-media/media.amp"
    print(datetime.datetime.now().strftime(
        "%c")[:-4], f"{func}: device url: {d_url}")
    d_name = device.json()["name"]
    api_host = f"{ip}:{port}"

    data = {
        "url": d_url,
        "name": d_name,
        "api_host": api_host
    }

    print(data) # 확인

    option = requests.post(
        f"http://{edge_ip}:{nodeport}/connect", data=json.dumps(data))
    option = option.text
    print(datetime.datetime.now().strftime(
        "%c")[:-4], f"{func}: browser option: {option}")
    # requests.post(
    #     f"http://192.168.0.29:5050/connect", data=json.dumps(data))
    print(datetime.datetime.now().strftime(
        "%c")[:-4], f"{func}: connecting completed !")
    print(datetime.datetime.now().strftime(
        "%c")[:-4], f"{func}:server name : {edge_name} --- camera name : {device_name}")

    res = jsonify(
        code="0000",
        message="처리 성공",
        url=f"http://{ip}:{nodeport}/streaming",
        sname=edge_name,
        option=option
    )
    return res


# 2.4 엣지서버에 연결된 디바이스 연결 해지
@ app.route('/disconnect_device', methods=['POST'])
def disconnect_device():
    func = sys._getframe().f_code.co_name
    print(datetime.datetime.now().strftime(
        "%c")[:-4], f"{func}: start")

    json_data = request.get_json(silent=True)
    if json_data == None:
        return response.message("0021")

    eid = json_data['eid']
    did = json_data['did']
    print(eid, did)

    device = requests.get(f"{API_URL}/get_deviceInfo?id={did}")
    device_name = device.json()["name"]

    edge = requests.get(f"{API_URL}/get_edgeInfo?id={eid}")
    edge_name = edge.json()["name"]
    edge_ip = edge.json()["ip"]

    print(
        datetime.datetime.now().strftime(
            "%c")[:-4], f"{func}: disconnect Server [{edge_name}] with device [{device_name}]....")

    # 노드포트 찾기위한 과정
    wids = db.session.query(Server_SW.wid).filter(eid == Server_SW.sid).all()
    for wid in wids:
        fname = db.session.query(SW_up.fname).filter(
            SW_up.sid == wid[0]).first()[0]
        if fname == "select-cam":
            sw_id = wid[0]

    nodeport = db.session.query(Server_SW.nodeport).filter(
        Server_SW.sid == eid, Server_SW.wid == sw_id).first()[0]

    # 디바이스 정보 추출
    d_url = "rtsp://keti:keti1234@" + \
        device.json()["ip"]+":"+device.json()["port"]+"/videomain"
    api_host = f"{ip}:{port}"

    data = {
        "url": d_url,
        "api_host": api_host
    }

    option = requests.post(
        f"http://{edge_ip}:{nodeport}/disconnect", data=json.dumps(data))

    # requests.post(
    #     f"http://192.168.0.29:5050/disconnect", data=json.dumps(data))
    print(datetime.datetime.now().strftime(
        "%c")[:-4], f"{func}: disconnecting completed !")
    print(datetime.datetime.now().strftime(
        "%c")[:-4], f"{func}: server name : {edge_name} --- camera name :  {device_name}")

    res = jsonify(
        code="0000",
        message="처리 성공",
        url=f"http://{ip}:{nodeport}/streaming",
        sname=edge_name

    )
    return res


# 2.5 마스터 서버가 저장하고 있는 업로드 소프트웨어 목록 조회
@ app.route('/get_uploadSwList', methods=['GET'])
def get_uploadSwList():

    sid_list = db.session.query(SW_up.sid).all()
    name_list = db.session.query(SW_up.name).all()
    fname_list = db.session.query(SW_up.fname).all()
    copyright_list = db.session.query(SW_up.copyright).all()
    type_list = db.session.query(SW_up.type).all()
    desc_list = db.session.query(SW_up.description).all()
    dt_list = db.session.query(SW_up.datetime).all()

    sw_list = []
    for sid in sid_list:
        sid = sid[0]
        name = db.session.query(SW_up.name).filter(SW_up.sid == sid).first()[0]
        fname = db.session.query(SW_up.fname).filter(
            SW_up.sid == sid).first()[0]
        copyright = db.session.query(SW_up.copyright).filter(
            SW_up.sid == sid).first()[0]
        type = db.session.query(SW_up.type).filter(SW_up.sid == sid).first()[0]
        desc = db.session.query(SW_up.description).filter(
            SW_up.sid == sid).first()[0]
        dt = db.session.query(SW_up.datetime).filter(
            SW_up.sid == sid).first()[0]

        sw = {
            "sid": sid,
            "name": name,
            "fname": fname,
            "copyright": copyright,
            "type": type,
            "description": desc,
            "datetime": dt
        }
        sw_list.append(sw)

    res = jsonify(
        code="0000",
        message="처리 성공",
        list=sw_list
    )
    return res


# 2.6 마스터 서버에 업로드된 소프트웨어 정보 조회
@ app.route('/get_uploadSwInfo', methods=['POST'])
def get_uploadSwInfo():

    json_data = request.get_json(silent=True)
    if json_data == None:
        return response.message("0021")

    sid = json_data['sid']

    name = db.session.query(SW_up.name).filter(SW_up.sid == sid).first()[0]
    fname = db.session.query(SW_up.fname).filter(SW_up.sid == sid).first()[0]
    copyright = db.session.query(SW_up.copyright).filter(
        SW_up.sid == sid).first()[0]
    type = db.session.query(SW_up.type).filter(SW_up.sid == sid).first()[0]
    desc = db.session.query(SW_up.description).filter(
        SW_up.sid == sid).first()[0]
    dt = db.session.query(SW_up.datetime).filter(SW_up.sid == sid).first()[0]

    res = jsonify(
        code="0000",
        message="처리 성공",
        name=name,
        fname=fname,
        copyright=copyright,
        type=type,
        description=desc,
        datetime=dt.strftime('%Y-%m-%d')
    )
    return res


# 2.7 마스터 서버에 업로드한 신규 소프트웨어 등록
@ app.route('/add_newUploadSw', methods=['POST'])
def add_newUploadSw():
    func = sys._getframe().f_code.co_name
    print(datetime.datetime.now().strftime(
        "%c")[:-4], f"{func}: start uploading a new software")
    json_data = request.get_json(silent=True)

    if json_data == None:
        return response.message("0021")

    name = json_data['name']
    copyright = json_data['copyright']
    type = json_data['type']
    desc = json_data['description']
    filename = json_data['file']

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

        zip_ref = zipfile.ZipFile(f"{fname}.zip")
        print(fname)
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
    else:
        fname = filename
        print(datetime.datetime.now().strftime(
            "%c")[:-4], f"{func}: software name: {fname}")
        with open(filename, 'wb') as file:
            data = requests.get(f"{API_URL}/download?filename={filename}")
            file.write(data.content)

    sid = sid_maker()
    q = db.session.query(SW_up).get(sid)  # sid 중복된게 있는지 찾아줌

    while q != None:
        sid = sid_maker()
        q = db.session.query(SW_up).get(sid)
        print(datetime.datetime.now().strftime(
            "%c")[:-4], f"{func}: re-generating software ID : {sid}")
        break
    else:
        print(datetime.datetime.now().strftime(
            "%c")[:-4], f"{func}: software ID : {sid}")

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


# 2.8 마스터 서버에 업로드된 SW 정보수정
@ app.route('/update_uploadSwInfo', methods=['POST'])
def update_uploadSwInfo():

    json_data = request.get_json(silent=True)
    if json_data == None:
        return response.message("0021")
    print(json_data)
    sid = json_data['sid']
    name = json_data['name']
    fname = json_data['fname']
    copyright = json_data['copyright']
    type = json_data['type']
    desc = json_data['description']

    sw = db.session.query(SW_up).filter(SW_up.sid == sid).update({
        'sid': sid,
        'name': name,
        'fname': fname,
        'copyright': copyright,
        'type': type,
        'description': desc
    })
    db.session.commit()

    return response.message("0000")


# 2.9 마스터 서버에 업로드된 SW 삭제
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


# 2.10 마스터/워커 서버에 배포된 SW 목록 조회
@ app.route('/get_deploySwList', methods=['POST'])
def get_deploySwList():

    json_data = request.get_json(silent=True)
    if json_data == None:
        return response.message("0021")

    sid = json_data['sid']
    sw_list = []

    s = db.session.query(Server_SW.wid).filter(sid == Server_SW.sid).all()
    for sw in s:
        Key = "wid"
        Value = sw[0]
        string = {Key: Value}
        sw_list.append(string)

    res = jsonify(
        code="0000",
        message="처리 성공",
        swList=sw_list
    )
    return res


# 2.11 마스터/워커 서버에 배포된 SW 정보 등록
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
    port = json_data['serviceport']
    node_port = json_data['nodeport']
    target_port = json_data['targetport']

    # fname 불러오기
    fname = db.session.query(SW_up.fname).filter(SW_up.sid == wid).first()[0]
    if "_" in fname:
        fname = fname.replace("_", "-")
    print(datetime.datetime.now().strftime(
        "%c")[:-4], f" {func}: software name is {fname}.....")

    if fname.find("prometheus") == 0:

        port = "8080"
        target_port = "9090"
        node_port = "30005"
        # node_selector.py 로 노드명 추가하는 기능 필요 test.py 에서 진행
        ns.select(fname, node_name)
        mm.namespace()
        mm.prometheus(fname)
        s = Server_SW(sid=sid, wid=wid, serviceport=port,
                      nodeport=node_port, targetport=target_port)
        db.session.add(s)
        db.session.commit()
        print("Deploy Completed!!")

        return response.message("0000")

    # select_cam 앱의 타겟포트 지정
    elif fname == "select-cam":
        target_port = "5050"
    elif fname == "edge-rtsp-sw":
        target_port = "5060"
    elif fname == "video-streaming":
        target_port = "5058"
    docker_id = "sehooh5"
    print(datetime.datetime.now().strftime(
        "%c")[:-4], f" {func}: Making deployment...")
    deployment = dm.making(fname, port, target_port,
                           node_port, node_name, docker_id)
    print(datetime.datetime.now().strftime(
        "%c")[:-4], f" {func}: ------ deployment ------ ")
    print(deployment)

    kubeconfig_path = f'$HOME/.kube/config'
    command = f"kubectl --kubeconfig={kubeconfig_path} apply -f {fname}-{node_name}.yaml"
    process = subprocess.run(command, shell=True, check=True, capture_output=True, text=True)
    print(process.stdout)
    print(process.stderr)


    print(datetime.datetime.now().strftime(
        "%c")[:-4], f" {func}: deploying {fname}-{node_name}.yaml.....")

    s = Server_SW(sid=sid, wid=wid, serviceport=port,
                  nodeport=node_port, targetport=target_port)
    db.session.add(s)
    db.session.commit()
    print(datetime.datetime.now().strftime(
        "%c")[:-4], f" {func}: deploy completed !")

    return response.message("0000")


# 2.12 마스터/워커 서버에 배포된 SW 삭제
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

    kubeconfig_path = f'$HOME/.kube/config'

    if "prometheus" in fname:
        os.system(f"kubectl --kubeconfig={kubeconfig_path} delete -f {fname}")
    else:
        command = f"kubectl --kubeconfig={kubeconfig_path} delete -f {fname}-{node_name}.yaml"
        process = subprocess.run(command, shell=True, check=True, capture_output=True, text=True)
        print(process.stdout)
        print(process.stderr)

    sw = db.session.query(Server_SW).filter(
        Server_SW.sid == sid, Server_SW.wid == wid).first()
    db.session.delete(sw)
    db.session.commit()
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


# (추가) 2.16 엣지 클러스터 삭제 인터페이스
@ app.route('/remove_edgeCluster', methods=['POST'])
def remove_edgeCluster():
    func = sys._getframe().f_code.co_name
    print(datetime.datetime.now().strftime(
        "%c")[:-4], f" {func}: deleting edge cluster")

    ips = []
    names = []
    hnames = []
    pwds = []
    node_types = []

    json_data = request.get_json(silent=True)
    if json_data == None:
        return response.message("0021")

    mid = json_data['mid']
    wlist = json_data['wlist']
    print(datetime.datetime.now().strftime(
        "%c")[:-4], f" {func}: master server ID : {mid}")

    if mid == None or wlist == None:
        return response.message("0015")

    res = requests.get(f"{API_URL}/get_edgeInfo?id={mid}")
    if res.json()["code"] != "0000":
        return response.message(res.json()["code"])
    ips.append(res.json()["ip"])
    names.append(res.json()["name"])
    hnames.append(res.json()["host_name"])
    pwds.append(res.json()["host_pwd"])
    node_types.append(res.json()["type"])

    for w in wlist:
        # 필요한 정보 얻기
        wid = w["wid"]
        print(datetime.datetime.now().strftime(
            "%c")[:-4], f" {func}: worker ID : {wid}")
        if wid == None:
            return response.message("0015")
        res = requests.get(f"{API_URL}/get_edgeInfo?id={wid}")

        ips.append(res.json()["ip"])
        names.append(res.json()["name"])
        hnames.append(res.json()["host_name"])
        pwds.append(res.json()["host_pwd"])
        node_types.append(res.json()["type"])

    print(datetime.datetime.now().strftime(
        "%c")[:-4], f" {func}: edge server list : {names}")

    for ip, name, hname, pwd, node_type in zip(ips, names, hnames, pwds, node_types):
        print(datetime.datetime.now().strftime(
        "%c")[:-4],f"{name} : delete node from cluster!")
        os.system(f"kubectl delete node {name}")

        # 0929
        # keti2(마스터)에서 ssh 연결시도시 Auth 에러떠서 따로 실행시킴
        if node_type == "Master":
            os.system("echo 'keti' | echo y | sudo kubeadm reset")
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

# 2.17 클러스터 모니터링 툴 추가 인터페이스
@ app.route('/add_newMonitoring', methods=['GET'])
def add_newMonitoring():
    func = sys._getframe().f_code.co_name
    print(datetime.datetime.now().strftime(
        "%c")[:-4], f" {func}: Grafana monitoring tool making")

    kubeconfig_path = f'$HOME/.kube/config'

    try:
        output = subprocess.check_output(
            f"kubectl --kubeconfig={kubeconfig_path} get ns monitoring", shell=True).decode('utf-8')
    except subprocess.CalledProcessError:
        output = "-1"
    if output == "-1":
        print(datetime.datetime.now().strftime(
            "%c")[:-4], f" {func}: Making Monitoring system by Prometheus and Grafana")
        mm.making(kubeconfig_path)

    print(datetime.datetime.now().strftime(
        "%c")[:-4], f" {func}: Monitoring tool making Completed")
    print(datetime.datetime.now().strftime(
        "%c")[:-4], f" {func}: Grafana url : http://{ip}:30006")

    res = jsonify(
        code="0000",
        message="처리 성공",
        url=f"http://{ip}:30006/d/JABGX_-mz/cluster-monitoring-for-kubernetes?orgId=1&refresh=10s"
    )
    return res



# 2.18 카메라 연결화면 조회 인터페이스
@ app.route('/get_camApp', methods=['GET'])
def get_camApp():

    res = jsonify(
        code="0000",
        message="처리 성공",
        url=f"http://{ip}:5000"
    )
    return res


# (추가) 스트리밍 화면이 꺼지고 난 후 환경변수 설정
@ app.route('/closed', methods=['GET'])
def closed():
    func = sys._getframe().f_code.co_name
    print(datetime.datetime.now().strftime(
        "%c")[:-4], f" {func}: start")

    json_data = json.loads(request.get_data(), encoding='utf-8')
    option = json_data['option']
    print(datetime.datetime.now().strftime(
        "%c")[:-4], f" {func}: Unloaded window! browser option : {option}")

    res = jsonify(
        code="0000",
        message="처리 성공",
        option=option
    )
    return res


@ app.route('/opened', methods=['GET'])
def opened():
    func = sys._getframe().f_code.co_name
    print(datetime.datetime.now().strftime(
        "%c")[:-4], f" {func}: start")

    json_data = json.loads(request.get_data(), encoding='utf-8')
    option = json_data['option']
    print(datetime.datetime.now().strftime(
        "%c")[:-4], f" {func}: Loaded window!! browser option : {option}")

    res = jsonify(
        code="0000",
        message="처리 성공",
        option=option
    )
    return res


@ app.route('/check', methods=['GET'])
def check():
    func = sys._getframe().f_code.co_name
    print(datetime.datetime.now().strftime(
        "%c")[:-4], f" {func}: Connect Server")
    time.sleep(1)
    print(datetime.datetime.now().strftime(
        "%c")[:-4], f" {func}: Connect Server")

    return datetime.datetime.now().strftime("%c")[:-4], f"{func}: Connect Server"


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
    app.run(host='0.0.0.0', threaded=True, port=port, debug=True)
