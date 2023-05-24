import requests
import sqlite3
import time
import os
import sys

num = sys.argv[1]
conn = sqlite3.connect(f"gps_0{num}.db", isolation_level=None, check_same_thread=False)
c = conn.cursor()

c.execute("SELECT COUNT(*) FROM gps_raw_data")
for row in c:
    num = row[0]
print(num)

# "bid": row[0],
# "time": row[1],
# "gps_raw_data": row[2]
while True:
    for num in range(1, num+1):
        if num == 1:
            print("데이터 초기화")
        c.execute(f"SELECT * FROM gps_raw_data WHERE ROWID={num}")
        for row in c:
            print(f"로우 데이터 {row[0]}: {row[2]}")



        time.sleep(0.5)

