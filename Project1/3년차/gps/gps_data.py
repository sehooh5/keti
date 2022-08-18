import serial
import pynmea2

def parseGPS(message):
    if (message[0:6] == "$GPGGA"):
        print("In")
        msg = pynmea2.parse(message)
        print(msg)
        print (f"Timestamp: {msg.timestamp} -- Lat: {msg.lat} {msg.lat_dir} " \
              f"-- Lon: {msg.lon} {msg.lon_dir} -- Altitude:{msg.altitude} {msg.altitude_units}")
    else :
        print("PASS")
serialPort = serial.Serial("/dev/ttyUSB0", 9600, timeout=0.5)
while True:
    msg = serialPort.readline()
    parseGPS(msg)