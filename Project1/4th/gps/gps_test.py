import sqlite3
import sys
import time

bnum = sys.argv[1]

conn = sqlite3.connect(f"gwg_test_SA_1.db", isolation_level=None, check_same_thread=False)
c = conn.cursor()

c.execute(f"SELECT lat, lon FROM gps_0{bnum}")
rows = c.fetchall()

for row in rows:
    lat, lon = row
#     print(f"GPS : {lat}, {lon}")

    sys.stdout.write(f"""\r

    
    lat : {lat}  lon : {lon}""")
    sys.stdout.flush()
    time.sleep(0.5)

c.close()
conn.close()