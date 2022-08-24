import socket
import json

port = 8080

server_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
server_socket.bind(('192.168.0.20', port))

while True:
    server_socket.listen()
    client_socket, addr = server_socket.accept()

    # 클라이언트로부터 메시지 받기
    recvData = client_socket.recv(65535)
    json_data = json.loads(recvData.decode(('utf-8')))
    type = json_data['type']
    print(json_data)

    if type == 'gps':
        print('gps 에서 데이터가 전달되었습니다!')
        sendData = 'GPS data uploaded!'
        client_socket.send(sendData.encode('utf-8'))
    elif type == 'vms':
        print('vms 에서 요청이 왔습니다!')
