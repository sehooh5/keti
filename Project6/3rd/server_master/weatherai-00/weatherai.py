# Weather AI 대체
import psutil
import requests
import json
import time

cnt = 0
res_class = "01"

def weather_sending():
    global cnt, res_class

    cnt+=1


    created_at = time.strftime("%Y-%m-%d %H:%M:%S", time.localtime())
    res_confidence = "0.8"

    if 1 <= cnt <= 30:
        res_class = "01"
    elif 31 <= cnt <= 59 :
        res_class = "02"
    elif cnt >= 60:
        res_class = "02"
        cnt = 0

    data = {
        "created_at": created_at,
        "res_class": res_class,
        "res_confidence": res_confidence
    }

    requests.post(f"http://192.168.0.14:6432/optimize_by_weather", json=data)

while True:
    weather_sending()
    time.sleep(1)


