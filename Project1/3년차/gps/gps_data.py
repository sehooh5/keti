import serial
import pynmea2

def parseGPS(message):
    if str.find('GGA') > 0:
        msg = pynmea2.parse(str)
        print(msg)
        print (f"Timestamp: {msg.timestamp} -- Lat: {msg.lat} {msg.lat_dir} " \
              f"-- Lon: {msg.lon} {msg.lon_dir} -- Altitude:{msg.altitude} {msg.altitude_units}")
    else:
        print("pass")

serialPort = serial.Serial("/dev/ttyUSB0", 9600, timeout=0.5)
while True:
    msg = serialPort.readline()
    print(msg)
    parseGPS(msg)