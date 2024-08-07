import ctypes
import requests
import traceback
import json
import sys
import time

# gps 로우데이터 저장기능 추가
import serial
import serial.tools.list_ports
import sqlite3
import time


# 사용 가능한 시리얼 포트 목록 찾기
ports = serial.tools.list_ports.comports()

# 사용 가능한 포트 출력
for port in ports:
    port = port.device

# 시리얼 포트 설정
ser = serial.Serial(port, 9600, timeout=1)

# GPS 데이터를 저장할 데이터베이스 연결
db_name = sys.argv[1]
conn = sqlite3.connect(f'{db_name}.db')
c = conn.cursor()

# 테이블 생성 (이미 생성되어 있다면 생략 가능)
c.execute('''CREATE TABLE IF NOT EXISTS gps_raw_data
             (id INTEGER PRIMARY KEY AUTOINCREMENT,
              timestamp DATETIME DEFAULT CURRENT_TIMESTAMP,
              raw_data BLOB)''')


url = "http://123.214.186.162:8088"

path = "./gwg.so"
c_module = ctypes.cdll.LoadLibrary(path)
# Global 변수 설정
global ss, ms

class STRUCT(ctypes.Structure) :
    _fields_ = [("yy", ctypes.c_uint),("mm", ctypes.c_uint),("dd", ctypes.c_uint),("hh", ctypes.c_uint),("mi", ctypes.c_uint),("ss", ctypes.c_uint),("ms", ctypes.c_uint),
                ("ax", ctypes.c_float),("ay", ctypes.c_float),("az", ctypes.c_float),("t", ctypes.c_float),
                ("wx", ctypes.c_float), ("wy", ctypes.c_float), ("wz", ctypes.c_float),
                ("roll", ctypes.c_float), ("pitch", ctypes.c_float), ("yaw", ctypes.c_float),
                ("mx", ctypes.c_float), ("my", ctypes.c_float), ("mz", ctypes.c_float),
                ("press", ctypes.c_float), ("h", ctypes.c_float),
                ("lon_final", ctypes.c_double), ("lat_final", ctypes.c_double),
                ("gh", ctypes.c_float), ("gy", ctypes.c_float), ("gv", ctypes.c_float),
                ("q0", ctypes.c_float), ("q1", ctypes.c_float), ("q2", ctypes.c_float),("q3", ctypes.c_float),
                ("sn", ctypes.c_float), ("pdop", ctypes.c_float), ("hdop", ctypes.c_float), ("vdop", ctypes.c_float)
                ]


str = STRUCT()

while True:
    # 시리얼 데이터 읽기
    raw_data = ser.readline()

    # 데이터가 존재하는 경우에만 처리
    if raw_data:

        # 데이터 출력
#         print(raw_data)
        # 데이터베이스에 쓰기
        c.execute("INSERT INTO gps_raw_data (raw_data) VALUES (?)", (raw_data,))
        conn.commit()

    time.sleep(0.5)
    try:
        c_module.process(ctypes.pointer(str)) # byref # 여기 C 과정에서 세그멘테이션 오류 발생
    except Exception as e:
        print(e)
        traceback.print_exc()

    ss = str.ss
    ms = str.ms
    data = {
        "time":{"yy": str.yy,"mm": str.mm,"dd": str.dd,"hh": str.hh,"mi": str.mi,"ss": str.ss,"ms": str.ms},
        "acc":{"ax":str.ax,"ay":str.ay,"az":str.az},
        "angular":{"wx":str.wx,"wy":str.wy,"wz":str.wz},
        "angle":{"roll":str.roll,"pitch":str.pitch,"yaw":str.yaw},
        "magnetic":{"mx": str.mx, "my": str.my, "mz": str.mz},
        "atmospheric":{"press": str.press, "h": str.h},
        "gps":{"lat_final": str.lat_final, "lon_final": str.lon_final},
        "groundSpeed":{"gh": str.gh, "gy": str.gy, "gv": str.gv},
        "quaternion":{"q0": str.q0, "q1": str.q1, "q2": str.q2, "q3": str.q3},
        "satelite":{"snum": str.sn, "pdop": str.pdop, "hdop": str.hdop, "vdop": str.vdop},
        "dbname":sys.argv[1],
    }
#     print(data)
    json_data = json.dumps(data)
    arg = sys.argv


    if len(arg) > 1 :
        requests.post(f'{url}/cgwg_save', json=json_data)
    else:
        requests.post(f'{url}/cgwg', json=json_data)

