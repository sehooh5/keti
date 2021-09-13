import requests
import json
from importlib import import_module
from flask import Flask, render_template, Response, request, jsonify
from flask_cors import CORS, cross_origin
import requests
import os
from models import db, SW_up, Server, Server_SW
import response
import string
import random
import paramiko
import getpass
import time
import socketio


app = Flask(__name__)
app.config['JSON_AS_ASCII'] = False  # jsonify 한글깨짐 해결

# 다른 서버에 명령 보낼때 사용
cli = paramiko.SSHClient()
cli.set_missing_host_key_policy(paramiko.AutoAddPolicy)


API_URL = "http://123.214.186.231:4882"


@app.route('/add_newEdgeCluster', methods=['POST'])
def add_newEdgeCluster():
    # 들어오는 정보
    json_data = request.get_json(silent=True)
    mid = json_data['mid']
    wlist = json_data['wlist']

    # POST (JSON)
    res = requests.get(f"{API_URL}/get_edgeInfo?id={mid}")
    mip = res.json()["ip"]
    print("mip : ", mip)
    # 마스터 엣지 구성
    m_output = os.system(
        f"sudo kubeadm init --pod-network-cidr=10.244.0.0/16 --apiserver-advertise-address={mip}")
    # 마스터 - 워커 연결해주는 명령어
    w_input = m_output.split('root:')[-1].lstrip()
    w_input = f"sudo {w_input}"
    # 마스터에서 설정해줘야 하는 내용
    os.system("mkdir -p $HOME/.kube")
    time.sleep(2.0)
    os.system("sudo cp -i /etc/kubernetes/admin.conf $HOME/.kube/config")
    time.sleep(2.0)
    os.system("sudo chown $(id -u):$(id -g) $HOME/.kube/config")
    time.sleep(2.0)
    os.system("kubectl apply -f https://raw.githubusercontent.com/coreos/flannel/master/Documentation/kube-flannel.yml")
    time.sleep(2.0)

    # 방법1. wlist에서 바로 정보쓰기
    for w in wlist:
        # 필요한 정보 얻기
        wid = w["wid"]
        res = requests.get(f"{API_URL}/get_edgeInfo?id={wid}")
        wip = res.json()["ip"]
        wname = res.json()["name"]
        wpwd = res.json()["type"]  # 지금은 type을 쓰지만 나중에 pwd 정보를 입력하고 저장된 정보를 사용

        # 워커노드와 연결
        cli.connect(wip), port = 22, username = wname, password = wpwd)
        stdin, stdout, stderr=cli.exec_command(w_input, get_pty = True)
        stdin.write('keti\n')
        stdin.flush()
        lines=stdout.readlines()
        print(''.join(lines))
        time.sleep(2.0)
        cli.close()

        print(f"마스터노드와 {wname} 노드 연결...ip 주소 : {wip}")


    return res.json()["ip"]


if __name__ == '__main__':
    app.run(host = '0.0.0.0', threaded = True, port = 5050)
