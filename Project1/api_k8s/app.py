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
import socket
# docker folder
from docker import build, push
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


# API URL "http://192.168.0.13:4882"
# API_URL = "http://123.214.186.231:4882"
API_URL = "http://192.168.0.69:4882"

# IP 주소
ips = subprocess.check_output("hostname -I", shell=True).decode('utf-8')
ip = ips.split(' ')[0]


@app.route('/')
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
            # n = {"nodename": name}
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
@app.route('/add_newEdgeCluster', methods=['POST'])
def add_newEdgeCluster():
    print("엣지 클러스터 구성중....")
    json_data = request.get_json(silent=True)
    print(json_data)
    if json_data == None:
        return response.message("0021")
    mid = json_data['mid']
    wlist = json_data['wlist']

    if mid == None or wlist == None:
        return response.message("0015")

    res = requests.get(f"{API_URL}/get_edgeInfo?id={mid}")
    if res.json()["code"] != "0000":
        return response.message(res.json()["code"])
    mip = res.json()["ip"]

    # 마스터 엣지 구성
    m_output = subprocess.check_output(
        f"echo keti | sudo -S kubeadm init --pod-network-cidr=10.244.0.0/16 --apiserver-advertise-address={mip}", shell=True).decode('utf-8')
    # 마스터 - 워커 연결해주는 명령어
    w_input = m_output.split('root:')[-1].lstrip()
    w_input = f"sudo {w_input}"
    # 마스터에서 설정해줘야 하는 내용
    os.system("mkdir -p $HOME/.kube")
    time.sleep(1.0)
    os.system("yes | sudo cp -i /etc/kubernetes/admin.conf $HOME/.kube/config")
    time.sleep(1.0)
    os.system("sudo chown $(id -u):$(id -g) $HOME/.kube/config")
    time.sleep(1.0)
    os.system("kubectl apply -f https://raw.githubusercontent.com/coreos/flannel/master/Documentation/kube-flannel.yml")
    time.sleep(1.0)

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

        print(f"마스터노드와 {host_name} 노드 연결...ip 주소 : {wip}")

    return response.message("0000")


# 2.2 엣지 서버 이름 조회 인터페이스
@ app.route('/get_edgeName', methods=['GET'])
def get_edgeName():

    nodes = subprocess.check_output(
        "kubectl get node", shell=True).decode('utf-8')

    nodes_split = nodes.split('\n')
    len_nodes = len(nodes_split)-1

    name_list = nodes_split[1:len_nodes]
    names = []
    for name in name_list:
        n = {"name": name.split(' ')[0]}
        names.append(n)

    res = jsonify(
        code="0000",
        message="처리 성공",
        nlist=names
    )
    return res


# 2.3 엣지서버에 디바이스 연결
@ app.route('/connect_device', methods=['POST'])
def connect_device():

    json_data = request.get_json(silent=True)
    if json_data == None:
        return response.message("0021")

    eid = json_data['eid']
    did = json_data['did']
    print(f"Connect Server [{eid}] with Device [{did}]....")

    device = requests.get(f"{API_URL}/get_deviceInfo?id={did}")
    device_name = device.json()["name"]

    edge = requests.get(f"{API_URL}/get_edgeInfo?id={eid}")
    edge_name = edge.json()["name"]

    # 노드포트 찾기위한 과정
    wids = db.session.query(Server_SW.wid).filter(eid == Server_SW.sid).all()
    for wid in wids:
        fname = db.session.query(SW_up.fname).filter(
            SW_up.sid == wid[0]).first()[0]
        if fname == "select-cam":
            sw_id = wid[0]

    nodeport = db.session.query(Server_SW.nodeport).filter(
        Server_SW.sid == eid, Server_SW.wid == sw_id).first()[0]
    print(f"Using Nodeport : {nodeport}")

    # 디바이스 정보 추출
    d_url = "rtsp://keti:keti1234@" + \
        device.json()["ip"]+":"+device.json()["port"]+"/videoMain"
    print(f"Device URL : {d_url}....")

    data = {
        "url": d_url
    }

    # requests.post(
    #     f"http://{ip}:{nodeport}/connect", data=json.dumps(data))
    requests.post(
        f"http://192.168.0.29:5000/connect", data=json.dumps(data))
    print("Connecting completed!! \n Camera streaming start...")
    print(f"Edge server : {edge_name} ------ Camera : {device_name}")

    res = jsonify(
        code="0000",
        message="처리 성공",
        url=f"http://{ip}:{nodeport}/streaming"
    )
    return res


# 2.4 엣지서버에 연결된 디바이스 연결 해지
@ app.route('/disconnect_device', methods=['POST'])
def disconnect_device():

    json_data = request.get_json(silent=True)
    if json_data == None:
        return response.message("0021")

    eid = json_data['eid']
    did = json_data['did']
    print(f"Discnnect Server [{eid}] with Device [{did}]....")

    device = requests.get(f"{API_URL}/get_deviceInfo?id={did}")
    device_name = device.json()["name"]

    edge = requests.get(f"{API_URL}/get_edgeInfo?id={eid}")
    edge_name = edge.json()["name"]

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

    data = {
        "url": d_url
    }

    # requests.post(
    #     f"http://{ip}:{nodeport}/connect", data=json.dumps(data))
    requests.post(
        f"http://192.168.0.29:5000/connect", data=json.dumps(data))
    print("Disconnecting completed!! \n Camera streaming end...")
    print(f"Edge server : {edge_name} ------ Camera : {device_name}")

    res = jsonify(
        code="0000",
        message="처리 성공",
        url=f"http://{ip}:{nodeport}/streaming"
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
        # dt = datetime[0].strftime('%Y-%m-%d')
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
@app.route('/get_uploadSwInfo', methods=['POST'])
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
@app.route('/add_newUploadSw', methods=['POST'])
def add_newUploadSw():
    print("Start uploading a new software..")
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

        print("Software name : ", fname)
        with open(f"{fname}.zip", 'wb') as select_cam:
            data = requests.get(f"{API_URL}/download?filename={filename}")
            select_cam.write(data.content)
        # print("select_cam : ", select_cam)

        zip_ref = zipfile.ZipFile(f"{fname}.zip")
        zip_ref.extractall(fname)
        zip_ref.close()
        print(f"{fname} file uploading completed!! \n Docker image building...")
        os.system(
            f"docker build -f {fname}/{fname} -t sehooh5/{fname}:latest .")
        print("Docker image building completed!! \n Docker image push to Docker hub..")
        os.system(f"docker push sehooh5/{fname}:latest")
        print("Docker image pushing completed!!")
    # elif filename.find("prometheus"):
    #     with open(filename, 'wb') as filename:
    #         data = requests.get(f"{API_URL}/download?filename={filename}")
    #         filename.write(data.content)
    else:
        fname = filename
        print(f"filename : {fname}")
        with open(filename, 'wb') as file:
            data = requests.get(f"{API_URL}/download?filename={filename}")
            file.write(data.content)

    sid = sid_maker()
    q = db.session.query(SW_up).get(sid)  # sid 중복된게 있는지 찾아줌

    while q != None:
        sid = sid_maker()
        q = db.session.query(SW_up).get(sid)
        print(f"Re-generating Software ID : {sid}")
        break
    else:
        print(f"Software ID : {sid}")

    # 2. software_up 테이블에 데이터 저장
    sw = SW_up(sid=sid, name=name, fname=fname,
               copyright=copyright, type=type, description=desc)
    db.session.add(sw)
    db.session.commit

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
    print("Deleting Uploaded Software...")
    json_data = request.get_json(silent=True)
    if json_data == None:
        return response.message("0021")

    sid = json_data['sid']

    fname = db.session.query(SW_up.fname).filter(SW_up.sid == sid).first()[0]
    print(f"Software ID : {sid} \n Software name : {fname}")

    # Docker image delete
    print(f"Docker image {fname} deleting...")
    os.system(f"docker rmi -f sehooh5/{fname}")
    print("Docker image deleted!!")

    sw = db.session.query(SW_up).filter(SW_up.sid == sid).first()

    db.session.delete(sw)
    db.session.commit()
    print("Software deleted!!")

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
    print("start deploying Software by Kubernetes...")

    json_data = request.get_json(silent=True)
    if json_data == None:
        return response.message("0021")
    wid = json_data['wid']  # SW ID
    sid = json_data['sid']  # Server ID
    print(
        f"Kubernetes : Deploy Software [{wid}] to Edge Server [{sid}]....")
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
    print(f"Software name is {fname}.....")

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
    docker_id = "sehooh5"
    print("Making deployment...")
    deployment = dm.making(fname, port, target_port,
                           node_port, node_name, docker_id)
    print("Deployment : ")
    print(deployment)

    os.system(f"kubectl apply -f {fname}-{node_name}.yaml")
    print(f"Deploying {fname}-{node_name}.yaml.....")

    s = Server_SW(sid=sid, wid=wid, serviceport=port,
                  nodeport=node_port, targetport=target_port)
    db.session.add(s)
    db.session.commit()
    print("Deploy Completed!!")

    return response.message("0000")


# 2.12 마스터/워커 서버에 배포된 SW 삭제
@ app.route('/remove_deploySwInfo', methods=['POST'])
def remove_deploySwInfo():

    json_data = request.get_json(silent=True)
    if json_data == None:
        return response.message("0021")
    print(json_data)
    wid = json_data['wid']
    sid = json_data['sid']
    print(
        f"Kubernetes : Undeploy Software [ID : {wid}] to Server [ID : {sid}]  ....")

    # 노드명 불러오기
    res = requests.get(f"{API_URL}/get_edgeInfo?id={sid}")
    if res.json()["code"] != "0000":
        return response.message(res.json()["code"])
    node_name = res.json()["name"]

    # fname 불러오기
    fname = db.session.query(SW_up.fname).filter(SW_up.sid == wid).first()[0]
    print(
        f"Undeploy Software [{fname}] from Server [{node_name}] ....")
    if fname.find("prometheus") == 0:
        os.system(f"kubectl delete -f {fname}")
    os.system(f"kubectl delete -f {fname}-{node_name}.yaml")

    sw = db.session.query(Server_SW).filter(
        Server_SW.sid == sid, Server_SW.wid == wid).first()
    db.session.delete(sw)
    db.session.commit()
    print("Undeploy Completed!!")

    return response.message("0000")


# 2.13 마스터 서버의 사용 가능한 서비스 포트 조회
@app.route('/get_servicePort', methods=['POST'])
def get_servicePort():

    json_data = request.get_json(silent=True)
    if json_data == None:
        return response.message("0021")

    cid = json_data['cid']
    print(cid)
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
            print(f"해당 포트번호는 사용중입니다. 포트번호를 재생성합니다 : {port}")
        else:
            print(f"해당 포트번호 사용 : {port}")
            break

    res = jsonify(
        code="0000",
        message="처리 성공",
        port=port
    )
    return res


# 2.14 마스터 서버의 사용 가능한 타깃 포트 조회
@app.route('/get_targetPort', methods=['POST'])
def get_targetPort():

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
            print(f"해당 포트번호는 사용중입니다. 포트번호를 재생성합니다 : {port}")
        else:
            print(f"해당 포트번호 사용 : {port}")
            break

    res = jsonify(
        code="0000",
        message="처리 성공",
        port=port
    )
    return res


# 2.15 마스터 서버의 사용 가능한 노드 포트 조회
@app.route('/get_nodePort', methods=['POST'])
def get_nodePort():

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
            print(f"해당 포트번호는 사용중입니다. 포트번호를 재생성합니다 : {port}")
        else:
            print(f"해당 포트번호 사용 : {port}")
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
    print("Deleting Edge Cluster....")
    ips = []
    names = []
    hnames = []
    pwds = []

    json_data = request.get_json(silent=True)
    if json_data == None:
        return response.message("0021")

    mid = json_data['mid']
    wlist = json_data['wlist']
    print(f"Master ID : {mid}...")

    if mid == None or wlist == None:
        return response.message("0015")

    res = requests.get(f"{API_URL}/get_edgeInfo?id={mid}")
    if res.json()["code"] != "0000":
        return response.message(res.json()["code"])
    ips.append(res.json()["ip"])
    names.append(res.json()["name"])
    hnames.append(res.json()["host_name"])
    pwds.append(res.json()["host_pwd"])

    for w in wlist:
        # 필요한 정보 얻기
        wid = w["wid"]
        print(f"Worker ID : {wid}...")
        if wid == None:
            return response.message("0015")
        res = requests.get(f"{API_URL}/get_edgeInfo?id={wid}")

        ips.append(res.json()["ip"])
        names.append(res.json()["name"])
        hnames.append(res.json()["host_name"])
        pwds.append(res.json()["host_pwd"])

    print(f"Edge Server List : {names}")

    for ip, name, hname, pwd in zip(ips, names, hnames, pwds):

        os.system(f"kubectl delete node {name}")

        cli.connect(ip, port=22, username=hname, password=pwd)

        stdin, stdout, stderr = cli.exec_command(
            "echo y | sudo kubeadm reset", get_pty=True)
        stdin.write('keti\n')
        stdin.flush()

        lines = stdout.readlines()
        print(''.join(lines))

        time.sleep(2.0)
        cli.close()

    print("Edge Cluster Deleted!!!")

    return response.message("0000")

# 2.17 클러스터 모니터링 툴 추가 인터페이스


@ app.route('/add_newMonitoring', methods=['GET'])
def add_newMonitoring():

    try:
        output = subprocess.check_output(
            "kubectl get ns monitoring", shell=True).decode('utf-8')
    except subprocess.CalledProcessError:
        output = "-1"
    if output == "-1":
        print("Making Monitoring system by Prometheus and Grafana")
        mm.making()

    print(
        f"Monitoring tool making Completed.. \n Grafana url : http://{ip}:30006")

    res = jsonify(
        code="0000",
        message="처리 성공",
        url=f"http://{ip}:30006"
    )
    return res

# 2.18 카메라 연결화면 조회 인터페이스


@app.route('/get_camApp', methods=['GET'])
def get_camApp():

    res = jsonify(
        code="0000",
        message="처리 성공",
        url=f"http://{ip}:5000"
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
    app.run(host='0.0.0.0', threaded=True, port=5000)
