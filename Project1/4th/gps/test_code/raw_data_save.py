import serial
import serial.tools.list_ports
import sqlite3
import time

# 사용 가능한 시리얼 포트 목록 찾기
ports = serial.tools.list_ports.comports()

# 사용 가능한 포트 출력
for port in ports:
    port = port.device

# 시리얼 포트 설정
ser = serial.Serial(port, 9600, timeout=1)

# GPS 데이터를 저장할 데이터베이스 연결
conn = sqlite3.connect('gps_data_test.db')
c = conn.cursor()

# 테이블 생성 (이미 생성되어 있다면 생략 가능)
c.execute('''CREATE TABLE IF NOT EXISTS gps_raw_data
             (id INTEGER PRIMARY KEY AUTOINCREMENT,
              timestamp DATETIME DEFAULT CURRENT_TIMESTAMP,
              raw_data TEXT)''')

# 무한 루프
while True:

    # 시리얼 데이터 읽기
    data = ser.readline()

    # 데이터가 존재하는 경우에만 처리
    if data:

        # 데이터 출력
        print(data)

        # 데이터베이스에 쓰기
        c.execute("INSERT INTO gps_raw_data (raw_data) VALUES (?)", (data,))
        conn.commit()

    # 0.5초 대기
    time.sleep(0.5)
