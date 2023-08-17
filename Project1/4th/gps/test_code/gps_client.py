import serial
import pynmea2
import datetime
import os
import socket
import json
import threading
import subprocess

port = 8088

def parseGPS(message):


    data = {
        'type': 'gps',
        'd_id': 'd1',
    }
    json_data = json.dumps(data)
    sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    sock.connect(('123.214.186.162', port))
    sock.send(json_data.encode('utf-8'))
    recvData = sock.recv(1024)
    data = recvData.decode(('utf-8'))
    print(data)

    message = message.decode('utf-8')
    if (message[0:6] == "$GPGGA"):
        msg = pynmea2.parse(message)

        gps_id = os.getlogin() # 서버의 username
        gps_time = datetime.datetime.utcnow().strftime("%m/%d/%Y, %H:%M:%S") # UTC 시간
        gps_lat = msg.lat
        gps_lon = msg.lon
        gps_lat_diumps(data)
        print(json_data)r = msg.lat_dir
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
        json_data = json.d
        sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        sock.connect(('123.214.186.162', port))
        sock.send(json_data.encode('utf-8'))
        recvData = sock.recv(1024)
        data = recvData.decode(('utf-8'))
        print(data)

    else :
        print("PASS")

serialPort = serial.Serial("/dev/ttyUSB0", 9600, timeout=5) # 임의로 5초 나중에 바꿔야함 1초로
while True:
    msg = serialPort.readline()
    parseGPS(msg)
