import psutil

# CPU 사용량 확인
cpu_percent = psutil.cpu_percent(interval=1)  # 1초 동안의 CPU 사용률을 백분율로 반환

# 메모리 사용량 확인
memory = psutil.virtual_memory()  # 가상 메모리 정보
memory_percent = memory.percent  # 메모리 사용률을 백분율로 반환

print(f"CPU 사용률: {cpu_percent}%")
print(f"메모리 사용률: {memory_percent}%")