# Sun 맑은날 AI

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


# cpu, memory, username 전송하는 기능
def cpu_mem_sending():
    # CPU 사용량 확인
    cpu_percent = psutil.cpu_percent(interval=1)  # 1초 동안의 CPU 사용률을 백분율로 반환

    # 메모리 사용량 확인
    memory = psutil.virtual_memory()  # 가상 메모리 정보
    memory_percent = memory.percent  # 메모리 사용률을 백분율로 반환

    data = {
        "code": "0000",
        "message": "처리성공",
        "username": username,
        "cpu": cpu_percent,
        "memory": memory_percent,
        "ai_class": "01",
        "version": "01"
    }
    json_data = json.dumps(data)

    requests.post(f"http://192.168.0.14:6432/usage", json=json_data)

while True:
    cpu_mem_sending()
    time.sleep(1)


