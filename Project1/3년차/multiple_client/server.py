import socket
import json

port = 8080

server_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
server_socket.bind(('localhost', port))
while True:
    server_socket.listen()
    client_socket, addr = server_socket.accept()

    # 클라이언트로부터 메시지 받기
    recvData = client_socket.recv(65535)
    json_data = json.loads(recvData.decode(('utf-8')))
    type = json_data['type'] 
    d_id = json_data['d_id']
    msg = json_data['msg']
    
    if type == 'sender':
        # sender 로 response
        print('이 장치는 sender 입니다!')
        sendData = 'ok'
        client_socket.send(sendData.encode('utf-8'))
    else :
        # device로 메시지 전송
        print('이 장치는 device 입니다!')
