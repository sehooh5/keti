


def parseGPS(message):
    message = message.decode('utf-8')
    if (message[0:6] == "$GPGGA"):
        msg = pynmea2.parse(message)

        gps_time = datetime.datetime.utcnow()
        gps_lat = msg.lat
        gps_lon = msg.lon
        gps_lat_dir = msg.lat_dir
        gps_lon_dir = msg.lon_dir
        gps_alt = msg.altitude
        gps_alt_units = msg.altitude_units

        print (f"Timestamp: {gps_time} -- Lat: {gps_lat} {gps_lat_dir} " \
              f"-- Lon: {gps_lon} {gps_lon_dir} -- Altitude:{gps_alt} {gps_alt_units}")
    else :
        print("PASS")

serialPort = serial.Serial("/dev/ttyUSB0", 9600, timeout=0.5)
while True:
    msg = serialPort.readline()
    parseGPS(msg)

