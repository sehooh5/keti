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
            print(num)
            print(row[0], row[1], row[2], row[3], row[4], row[5])
                # data = {
                #     "cid": cid,
                #     "gps" : {
                #         "lat": lat_row,
                #         "lat_dir": row[1],
                #         "lon": lon_row,
                #         "lon_dir": row[3],
                #         "alt": row[4],
                #         "alt_units": row[5],
                #     },
                # }
                # requests.post(f'{url}/gps_temp', json=data)

        time.sleep(1)

