import requests
import serial
import pynmea2
import datetime
import os
import socket
import json
import sys

url = "http://123.214.186.162:8088"

data = {
    "did": "keti0"
}

def parseGPS(message):
    message = message.decode('utf-8')
    if (message[0:6] == "$GPGGA"):
        msg = pynmea2.parse(message)

        gps_id = os.getlogin()  # 서버의 username
        gps_time = datetime.datetime.utcnow().strftime("%m/%d/%Y, %H:%M:%S")  # UTC 시간
        gps_lat = msg.lat
        gps_lon = msg.lon
        gps_lat_dir = msg.lat_dir
        gps_lon_dir = msg.lon_dir
        gps_alt = msg.altitude
        gps_alt_units = msg.altitude_units

        data = {
            'type': 'gps',
            'gps_id': gps_id,
            'gps_time': gps_time,
            'gps_lat': gps_lat,
            'gps_lon': gps_lon,
            'gps_lat_dir': gps_lat_dir,
            'gps_lon_dir': gps_lon_dir,
            'gps_alt': gps_alt,
            'gps_alt_units': gps_alt_units
        }
        json_data = json.dumps(data)

        arg = sys.argv[1]
        print(arg[1], type(arg[1]))
        res = requests.post(f'{url}/{arg[1]}', json=data)
        # gps 데이터 저장 없이 삭제하는 API
        # res = requests.post(f'{url}/gps', json=data)
        # gps 데이터 DB에 저장하는 API
        # res = requests.post(f'{url}/gps_save', json=data)

        return res

serialPort = serial.Serial("/dev/ttyUSB0", 9600, timeout=5) # 임의로 5초 나중에 바꿔야함 1초로
while True:
    msg = serialPort.readline()
    parseGPS(msg)