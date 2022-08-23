import serial
import pynmea2

def parseGPS(message):
    print(message)
    if (message[0:6] == "$GPGGA"):
        print("IN")
        msg = pynmea2.parse(message)
        print(msg)
        print (f"Timestamp: {msg.timestamp} -- Lat: {msg.lat} {msg.lat_dir} " \
              f"-- Lon: {msg.lon} {msg.lon_dir} -- Altitude:{msg.altitude} {msg.altitude_units}")
    else :
        print("PASS")
serialPort = serial.Serial("/dev/ttyUSB0", 9600, timeout=0.5)
while True:
    msg = serialPort.readline()
    # print(type(msg))
    # m = pynmea2.parse(msg.decode('utf-8'))
    # print(m)

    parseGPS(msg)



######### 현재 parseGPS if 문 안으로 안들어감 왜그런지 해결해야함!!!!