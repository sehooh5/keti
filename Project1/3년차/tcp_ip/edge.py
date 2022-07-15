import socket
import json
import time
import threading
import os
import subprocess

port = 8080

def edge():
    # 소켓 서버로 보낼 데이터
    data = {
        'type': 'edge',
        'e_id': 'e1',
    }
    json_data = json.dumps(data)

    sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    sock.connect(('192.168.0.20', port))
    sock.send(json_data.encode('utf-8'))
    recvData = sock.recv(1024)
    data = recvData.decode(('utf-8'))
    if data == "None":
        print(data)
    else:
        json_data = json.loads(recvData.decode(('utf-8')))
        print("json_data", json_data)
        d_ip = json_data['d_ip']
        print('d_ip : ', d_ip)
        e_ip = json_data['e_ip']
        print('e_ip : ', e_ip)
        
        # d_ip 의 rtsp 영상을 가지고 e_ip로 rtp 보내는 명령어
        subprocess.call('cvlc -vvv rtsp://keti:keti1234@192.168.0.46:88/videoMain --sout="#rtp{dst=192.168.0.60,port=5004,mux=ts}" --no-sout-all --sout-keep', shell=True)

    threading.Timer(1, edge).start()

edge()
