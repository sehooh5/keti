import socket
import json

port = 8088

server_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
server_socket.bind(("123.214.186.162", port))
print("123.214.186.162:8080 서버 생성")

while True:
    server_socket.listen()
    client_socket, addr = server_socket.accept()
    print("client socket 연결됨")
    
    # 클라이언트로부터 메시지 받기
    recvData = client_socket.recv(65535)
    json_data = json.loads(recvData.decode(('utf-8')))
    type = json_data['type']
    print(json_data)

    if type == 'gps':
        print('gps 에서 데이터가 !')
        sendData = 'GPS data uploaded!'
        client_socket.send(sendData.encode('utf-8'))
    elif type == 'vms':
        print('vms 에서 요청이 왔습니다!')
