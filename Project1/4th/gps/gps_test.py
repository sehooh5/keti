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
    lines = []

    lines.append("  [GPS DATA]")
    lines.append(f"  lat : {lat}  lon : {lon}")

    for line in lines:
        sys.stdout.write(f"\r{line} ")
        sys.stdout.flush()
        time.sleep(0.5)

c.close()
conn.close()