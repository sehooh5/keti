import socket
import json
import sqlite3

port = 8080

# DB 생성 (오토 커밋)
conn = sqlite3.connect("test.db", isolation_level=None)
# 커서 획득
c = conn.cursor()

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
        print(f'이 장치의 메시지는 [Device ID : {d_id}] 로 전달됩니다!')

        c.execute('select name from sqlite_master where type="table" and name="d1"')
        t_exist = c.fetchone()
        if t_exist == 'None': #d_id 테이블이 없으면 테이블 생성
            c.execute(f"CREATE TABLE IF NOT EXISTS {d_id} \
                (id integer PRIMARY KEY, msg text)")
        # d_id 테이블이 있으면 데이터 저장
        c.execute(f"SELECT max(id) FROM {d_id}")
        max_id = c.fetchone()[0] # 가장 큰 id 값

        
        

        sendData = 'ok'
        client_socket.send(sendData.encode('utf-8'))
    else:
        # device로 메시지 전송
        print('이 장치는 device 입니다!')
        print(f'이 장치의 ID는 {d_id} 입니다!')
