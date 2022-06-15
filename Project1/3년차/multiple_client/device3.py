import socket
import json
import time
import threading

port = 8080

def device():
    # 소켓 서버로 보낼 데이터
    data = {
        'type': 'device',
        'd_id': 'd3',
        'msg': 'data from device d3'
    }
    json_data = json.dumps(data)
    # print(json_data)

    sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    sock.connect(('localhost', port))
    sock.send(json_data.encode('utf-8'))
    recvData = sock.recv(1024)
    print('응답 : ', recvData.decode('utf-8'))
    threading.Timer(1, device).start()

device()
