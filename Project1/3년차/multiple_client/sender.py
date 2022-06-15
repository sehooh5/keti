import socket
import json
from datetime import datetime
import sys

now = datetime.now()
current_time = now.strftime("%H:%M:%S")

port = 8080

d_id = sys.argv[1]

# 소켓 서버로 보낼 데이터
data = {
    'type': 'sender',
    'd_id': d_id,
    'msg': f'data for [{d_id}] / {current_time}'
}
json_data = json.dumps(data)

sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
sock.connect(('localhost', port))
sock.send(json_data.encode('utf-8'))
recvData = sock.recv(1024)
print('응답 : ', recvData.decode('utf-8'))
