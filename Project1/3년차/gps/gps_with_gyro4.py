import ctypes
import requests
import time

url = "http://123.214.186.162:8088"

path = "./gwg4.so"
c_module = ctypes.cdll.LoadLibrary(path)
# Global 변수 설정
global ss, ms

def req_post(url):
    print(f'Request POST to : {url}')
    print(ss, ms)
    res = requests.get(f'{url}/')
    return res

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
                ("sn", ctypes.c_float), ("pdop", ctypes.c_float), ("hdop", ctypes.c_float), ("vdop", ctypes.c_float),
                ]


str = STRUCT()
while True:
    time.sleep(0.5)
    c_module.process(ctypes.pointer(str))
    print("입력된 데이터 : ")
    print(str.mi, str.ss, str.ms, str.ax, str.ay, str.az, str.lat_final, str.lon_final)

    ss = str.ss
    ms = str.ms
    res = req_post(url)
    print(res)
