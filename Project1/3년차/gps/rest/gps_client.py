import serial
import pynmea2
import datetime
import os
from flask import Flask, render_template, Response, request, jsonify
import json
import requests
import response

app = Flask(__name__)
port = 5885

@app.route('/')
def index():
    return "index"

@app.route('/get_gpsInfo', methods=['GET'])
def gps():
    serialPort = serial.Serial("/dev/ttyUSB0", 9600, timeout=5)
    msg = serialPort.readline()
    res = parseGPS(msg)
    print(res)

    return res

app.run(host="192.168.225.27",port=port)
#192.168.225.27

def parseGPS(message):

    message = message.decode('utf-8')
    if (message[0:6] == "$GPGGA"):
        msg = pynmea2.parse(message)

        gps_id = os.getlogin() # 서버의 username
        gps_time = datetime.datetime.utcnow().strftime("%m/%d/%Y, %H:%M:%S") # UTC 시간
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
        print(json_data)
    return json_data
        #print (f"ID: {gps_id} -- Timestamp: {gps_time} -- Lat: {gps_lat} {gps_lat_dir} " \
        #      f"-- Lon: {gps_lon} {gps_lon_dir} -- Altitude:{gps_alt} {gps_alt_units}")


#serialPort = serial.Serial("/dev/ttyUSB0", 9600, timeout=5) # 임의로 5초 나중에 바꿔야함 1초로
#while True:
#    msg = serialPort.readline()
#    parseGPS(msg)
