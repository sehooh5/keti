import requests
import sqlite3
import time
import os

url = "http://123.214.186.162:8088"
conn = sqlite3.connect("gwg_test.db", isolation_level=None, check_same_thread=False)
c = conn.cursor()

c.execute("SELECT COUNT(*) FROM gwg_save")
for row in c:
    num = row[0]

while True:
    for num in range(1, num+1):
        if num == 1:
            print("데이터 초기화")
        c.execute(f"SELECT * FROM gwg_save WHERE ROWID={num}")
        for row in c:
            data = {
                "code": "0000",
                "message": "처리 성공",
                "time" : {"yy":row[0], "mm":row[1],"dd":row[2],"hh":row[3],"mi":row[4],"ss":row[5],"ms":row[6]},
                "acc" : {"ax":row[7],"ay":row[8],"az":row[9]},
                "angular": {"wx": row[10], "wy": row[11], "wz": row[12]},
                "angle": {"roll":row[13], "pitch":row[14], "yaw":row[15]},
                "magnetic": {"mx": row[16], "my": row[17], "mz": row[18]},
                "atmospheric": {"press": row[19], "h": row[20]},
                "gps": {"lat": row[21], "lon": row[22]},
                "groundspeed": {"gh": row[23], "gy": row[24], "gv": row[25]},
                "quaternion": {"q0": row[26], "q1": row[27], "q2": row[28], "q3": row[29]},
                "satelite": {"snum": row[30], "pdop": row[31], "hdop": row[32], "vdop": row[33]}
            }
            # print(data)

            requests.post(f'{url}/gwg_temp', json=data)

        time.sleep(1)

