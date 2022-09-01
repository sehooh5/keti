import requests
import serial
import pynmea2
import datetime
import os
import sys

url = "http://123.214.186.162:8088"


def parseGPS(message):
    message = message.decode('utf-8')
    if (message[0:6] == "$GPGGA"):
        msg = pynmea2.parse(message)

        if msg.lat == "" :
            print("실내에서 GPS가 작동하지 않음")
        else:
            gps_id = os.getlogin()  # 서버의 username
            gps_time = datetime.datetime.utcnow().strftime("%m/%d/%Y, %H:%M:%S")  # UTC 시간
            gps_lat = str(round(float(msg.lat)/100, 6))
            gps_lon = str(round(float(msg.lon)/100, 6))
            gps_lat_dir = msg.lat_dir
            gps_lon_dir = msg.lon_dir
            gps_alt = msg.altitude
            gps_alt_units = msg.altitude_units
            print(f"lat : {gps_lat}, lon : {gps_lon}")

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

            arg = sys.argv

            # argument 에 따라 서버에 데이터 저장할지 안할지 선택
            if len(arg) < 2 :
                res = requests.post(f'{url}/gps', json=data)
                # print(res.text)
            else :
                res = requests.post(f'{url}/gps_save', json=data)
                # print(res.text)
            return res
    # elif (message[0:6] == "$GPRMC"):
    #     msg = pynmea2.parse(message)
    #
    #     print(f"lat : {msg.lat}, lon : {msg.lon}")
for f_name in os.listdir('/dev'):
    if f_name.startswith('ttyUSB'):
        global fname
        fname = f_name
serialPort = serial.Serial(f"/dev/{fname}", 9600, timeout=5) # 임의로 5초 나중에 바꿔야함 1초로
while True:
    msg = serialPort.readline()
    parseGPS(msg)