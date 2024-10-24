import psutil
import requests
import json
import time

def cpu_mem_sending():
    # CPU 사용량 확인
    cpu_percent = psutil.cpu_percent(interval=1)  # 1초 동안의 CPU 사용률을 백분율로 반환

    # 메모리 사용량 확인
    memory = psutil.virtual_memory()  # 가상 메모리 정보
    memory_percent = memory.percent  # 메모리 사용률을 백분율로 반환

    data = {
        "code": "0000",
        "message": "처리성공",
        "did": "dx01", # 나중에 변경해야함
        "cpu": cpu_percent,
        "memory" : memory_percent
    }
    json_data = json.dumps(data)

    requests.post(f"http://123.214.186.162:6432/usage", json=json_data)

while True:
    cpu_mem_sending()
    time.sleep(1)


