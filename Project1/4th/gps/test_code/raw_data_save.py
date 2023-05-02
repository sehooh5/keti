import serial
import serial.tools.list_ports

# 사용 가능한 시리얼 포트 목록 찾기
ports = serial.tools.list_ports.comports()

# 사용 가능한 포트 출력
for port in ports:
    port = port.device

# 시리얼 포트 설정
ser = serial.Serial(port, 9600, timeout=1)

# GPS 데이터를 저장할 파일 열기
with open('gps_data.txt', 'w') as file:
    while True:
            line = ser.readline().decode("utf-8")
            file.write(line)