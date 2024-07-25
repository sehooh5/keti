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

    print(f"CPU Usage : {cpu_percent}%, Memory Usage : {memory_percent}%")

while True:
    cpu_mem_sending()
    time.sleep(1)


