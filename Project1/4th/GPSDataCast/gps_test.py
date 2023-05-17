import requests
import sqlite3
import time
import os

url = "http://123.214.186.162:8089"
conn = sqlite3.connect("gps_01.db", isolation_level=None, check_same_thread=False)
c = conn.cursor()

c.execute("SELECT COUNT(*) FROM gps_raw_data")
for row in c:
    num = row[0]
print(num)

while True:
    for num in range(1, num+1):
        if num == 1:
            print("데이터 초기화")
        c.execute(f"SELECT * FROM gps_raw_data WHERE ROWID={num}")
        for row in c:
            print(f'{row[0]}, {row[1]}, {row[2]}')
            data = {
                "code": "0000",
                "message": "처리 성공",
                "bid": row[0],
                "time": row[1],
                "gps_raw_data": row[2]
            }
            requests.post(f'{url}/gwg_temp', json=data)

        time.sleep(0.5)

