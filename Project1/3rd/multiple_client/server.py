import socket
import json
import sqlite3

port = 8080

# DB 생성 (오토 커밋)
conn = sqlite3.connect("test3.db", isolation_level=None)

# 커서 획득
c = conn.cursor()

server_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
server_socket.bind(('192.168.0.20', port))
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

        c.execute(f'select name from sqlite_master where type="table" and name="{d_id}"')
        t_exist = c.fetchone()
        # d_id 테이블이 없으면 테이블 생성
        if t_exist == None:
            print(f"{d_id} 테이블 생성")
            c.execute(f"CREATE TABLE IF NOT EXISTS {d_id} \
                (id integer PRIMARY KEY, msg text)")
        # d_id 테이블이 있으면 데이터 저장
        print(f"{d_id} 테이블에 데이터 저장")
        # 테이블에 데이터가 있는지 없는지부터 확인
        c.execute((f"SELECT COUNT(*) from {d_id}"))
        count = c.fetchall()[0][0]
        if count == 0:
            mid = 1
        else:
            c.execute(f"SELECT max(id) FROM {d_id}")
            mid = c.fetchone()[0] + 1  # 가장 큰 id 값

        c.execute(f"INSERT INTO {d_id} \
            VALUES(?,?)", (mid, msg))
     
        sendData = 'ok'
        client_socket.send(sendData.encode('utf-8'))
    else:
        # device로 메시지 전송
        print(f'이 장치는 device {d_id} 입니다!')
        # 테이블이 있는지 확인
        c.execute(f'select name from sqlite_master where type="table" and name="{d_id}"')
        t_exist = c.fetchone()
        # 테이블이 없으면 생성
        if t_exist == None:
            print(f"{d_id} 테이블 생성")
            c.execute(f"CREATE TABLE IF NOT EXISTS {d_id} \
                            (id integer PRIMARY KEY, msg text)")
        c.execute(f"SELECT min(id) FROM {d_id}")
        # 가장 작은 id 값
        mid = c.fetchone()[0]
        # 테이블에 데이터가 없으면 None 을 response
        if mid == None:
            msg = "None"
            client_socket.send(msg.encode('utf-8'))
        else:
            # device 로 전송할 메시지 추출
            c.execute(f"SELECT msg FROM {d_id} WHERE id={mid}")
            msg = c.fetchone()[0]
            # 소켓 사용해서 전송
            client_socket.send(msg.encode('utf-8'))
            # db에서 data 삭제
            c.execute(f"DELETE FROM {d_id} WHERE id=?", (mid,))

