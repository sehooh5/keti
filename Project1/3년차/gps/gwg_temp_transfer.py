import requests
import sqlite3
import time
import os

url = "http://123.214.186.162:8088"
conn = sqlite3.connect("gwg_test.db", isolation_level=None, check_same_thread=False)
c = conn.cursor()

num = c.execute("SELECT COUNT(*) FROM gwg_save")
print(num)
# while True:
#     for num in range(950, 2667):
#         if num == 950:
#             print("데이터 초기화")
#         c.execute(f"SELECT * FROM keti0_save WHERE ROWID={num}")
#         for row in c:
#             if row[0] == "":
#                 pass
#             else:
#                 lat_row = str(round(float(row[0]) / 100 + 0.232578, 6))
#                 lon_row = str(round(float(row[2]) / 100 + 0.353769, 6))
#                 cid = os.getlogin()
#                 print(lat_row, lon_row)
#
#                 data = {
#                     "cid": cid,
#                     "gps" : {
#                         "lat": lat_row,
#                         "lat_dir": row[1],
#                         "lon": lon_row,
#                         "lon_dir": row[3],
#                         "alt": row[4],
#                         "alt_units": row[5],
#                     },
#                 }
#                 requests.post(f'{url}/gps_temp', json=data)
#
#         time.sleep(1)

