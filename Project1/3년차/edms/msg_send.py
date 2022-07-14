import socket
import json
from datetime import datetime
import sys
import sqlite3

# DB 생성 (오토 커밋)
conn = sqlite3.connect("test1.db", isolation_level=None)
c = conn.cursor()

now = datetime.now()
current_time = now.strftime("%H:%M:%S")

port = 8080

d_id = sys.argv[1]
e_id = sys.argv[2]

# d_id 로 DB 에서 device 의 rtsp 주소 찾기
c.execute(f"SELECT ip FROM device WHERE id='{d_id}'")
d_ip = c.fetchone()
print("Device IP : ", d_ip)

# e_id 로 DB 에서 edge server 의 ip 주소 찾기
c.execute(f"SELECT ip FROM edge WHERE id='{e_id}'")
e_ip = c.fetchone()
print("Edge IP : ", e_ip)

# 소켓 서버로 보낼 데이터
data = {
    'type': 'sender',
    'd_id': d_id,
    'd_ip': d_ip,
    'e_id': e_id,
    'e_ip': e_ip,
}
json_data = json.dumps(data)
print(json_data)

sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
sock.connect(('192.168.0.20', port))
sock.send(json_data.encode('utf-8'))
recvData = sock.recv(1024)
print('응답 : ', recvData.decode('utf-8'))
