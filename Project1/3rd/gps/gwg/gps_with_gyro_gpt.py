import ctypes
import traceback
import sys

import threading
import json
import requests

from collections import namedtuple

url = "http://123.214.186.162:8088"
path = "./gwg.so"
c_module = ctypes.cdll.LoadLibrary(path)

class Struct:
    def __init__(self):
        self.time = {"yy": 0, "mm": 0, "dd": 0, "hh": 0, "mi": 0, "ss": 0, "ms": 0}
        self.acc = {"ax": 0.0, "ay": 0.0, "az": 0.0}
        self.angular = {"wx": 0.0, "wy": 0.0, "wz": 0.0}
        self.angle = {"roll": 0.0, "pitch": 0.0, "yaw": 0.0}
        self.magnetic = {"mx": 0.0, "my": 0.0, "mz": 0.0}
        self.atmospheric = {"press": 0.0, "h": 0.0}
        self.gps = {"lat_final": 0.0, "lon_final": 0.0}
        self.groundSpeed = {"gh": 0.0, "gy": 0.0, "gv": 0.0}
        self.quaternion = {"q0": 0.0, "q1": 0.0, "q2": 0.0, "q3": 0.0}
        self.satelite = {"snum": 0.0, "pdop": 0.0, "hdop": 0.0, "vdop": 0.0}

str = Struct()
def process_data():

    while True:
        try:
            c_module.process(ctypes.byref(str))
        except Exception as e:
            print(e)
            traceback.print_exc()

        data = Data(
            time={"yy": str.yy, "mm": str.mm, "dd": str.dd, "hh": str.hh, "mi": str.mi, "ss": str.ss, "ms": str.ms},
            acc={"ax": str.ax, "ay": str.ay, "az": str.az},
            angular={"wx": str.wx, "wy": str.wy, "wz": str.wz},
            angle={"roll": str.roll, "pitch": str.pitch, "yaw": str.yaw},
            magnetic={"mx": str.mx, "my": str.my, "mz": str.mz},
            atmospheric={"press": str.press, "h": str.h},
            gps={"lat_final": str.lat_final, "lon_final": str.lon_final},
            groundSpeed={"gh": str.gh, "gy": str.gy, "gv": str.gv},
            quaternion={"q0": str.q0, "q1": str.q1, "q2": str.q2, "q3": str.q3},
            satelite={"snum": str.sn, "pdop": str.pdop, "hdop": str.hdop, "vdop": str.vdop}
        )

        print(data)

        with requests.Session() as session:
            json_data = json.dumps(data._asdict())
            arg = sys.argv
            if len(arg) > 1:
                session.post(f'{url}/cgwg_save', json=json_data)
            else:
                session.post(f'{url}/cgwg', json=json_data)

def main():
    t = threading.Thread(target=process_data)
    t.start()

if __name__ == '__main__':
    main()
