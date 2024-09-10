# Weather AI 대체
import psutil
import requests
import json
import time
import subprocess

result = subprocess.run(['whoami'], capture_output=True, text=True)

if result.returncode == 0:
    username = result.stdout.strip()
    print(f"Current user: {username}")
else:
    print(f"Error: {result.stderr}")

cnt = 0
res_class = "01"

# cpu, memory, username 전송하는 기능
def weather_sending():
    global cnt, res_class

    cnt+=1

    nid = "ni01"
    created_at = time.strftime("%Y-%m-%d %H:%M:%S", time.localtime())
    res_confidence = "0.8"

    if cnt < 30:
        res_class = "01"
    elif cnt >= 30:
        res_class = "02"
        cnt = 0

    data = {
        "nid": nid,
        "created_at": created_at,
        "res_class": res_class,
        "res_confidence": res_confidence
    }
    json_data = json.dumps(data)

    requests.post(f"http://192.168.0.14:6432/save_edgeData", json=json_data)
    print(f"Sent data: {json_data}, Response: {response.status_code}")

while True:
    weather_sending()
    time.sleep(1)


