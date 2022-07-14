import socket
import json
import time
import threading

port = 8080

def device():
    # 소켓 서버로 보낼 데이터
    data = {
        'type': 'device',
        'd_id': 'd1',
    }
    json_data = json.dumps(data)
    # print(json_data)

    sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    sock.connect(('192.168.0.20', port))
    sock.send(json_data.encode('utf-8'))
    recvData = sock.recv(1024)
    json_data = json.loads(recvData.decode(('utf-8')))
    d_ip = json_data['d_ip']
    print('d_ip : ', d_ip)
    e_ip = json_data['e_ip']
    print('e_ip : ', e_ip)
    threading.Timer(1, device).start()

device()
