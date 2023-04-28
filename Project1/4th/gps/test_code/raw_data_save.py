import serial

# 시리얼 포트 설정
ser = serial.Serial('/dev/ttyUSB0', 9600, timeout=1)

# GPS 데이터를 저장할 파일 열기
with open('gps_data.txt', 'w') as file:

    # 무한 루프
    while True:

        # 시리얼 데이터 읽기
        data = ser.readline()

        # 데이터가 존재하는 경우에만 처리
        if data:

            # 데이터 출력
            print(data)

            # 데이터 파일에 쓰기
            file.write(data + '\n')