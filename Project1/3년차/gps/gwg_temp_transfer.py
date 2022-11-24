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
            data = {
                "time" : {"yy":row[0], "mm":row[1],"dd":row[2],"hh":row[3],"mi":row[4],"ss":row[5],"ms":row[6]}
                ,
            }
            print(data)
            print(type(row[0]))
            print(type(data))
            # requests.post(f'{url}/gps_temp', json=data)

        time.sleep(1)

