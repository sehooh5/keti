import socket
import json

port = 8080

# 소켓 서버로 보낼 데이터
data = {
    'type': 'sender',
    'd_id': 'd1',
    'msg': 'data from sender'
}
json_data = json.dumps(data)
print(json_data)

sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
sock.connect(('localhost', port))
sock.send(json_data.encode('utf-8'))
recvData = sock.recv(1024)
print('응답 : ', recvData)
