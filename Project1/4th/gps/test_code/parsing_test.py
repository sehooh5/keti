import struct

# 바이너리 데이터를 읽어옵니다.
data = b'\x08\\\x0c\x04UR\x00\x00\x00\x00\x00\x00\\\x0c\x0fUS~\xff<\x00\xff\xff\xb8F]UT\x90\x01\xeb\xfa\x88\xe4\\\x0c\xf3UU\xff\x0f\xff\x0f\xaa\n'

# 바이트 단위로 데이터를 추출합니다.
time = struct.unpack('<L', data[:4])[0]  # 4바이트의 unsigned long 형식으로 저장된 시간 정보
latitude = struct.unpack('<f', data[4:8])[0]  # 4바이트의 float 형식으로 저장된 위도 정보
longitude = struct.unpack('<f', data[8:12])[0]  # 4바이트의 float 형식으로 저장된 경도 정보
altitude = struct.unpack('<f', data[12:16])[0]  # 4바이트의 float 형식으로 저장된 고도 정보

# 결과를 출력합니다.
print(f'Time: {time}')
print(f'Latitude: {latitude}')
print(f'Longitude: {longitude}')
print(f'Altitude: {altitude}')