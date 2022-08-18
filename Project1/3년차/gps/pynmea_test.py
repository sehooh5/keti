import pynmea2

str = "$GPGGA,071341.000,3734.8517,N,12653.2973,E,1,8,0.99,79.5,M,19.2,M,,*61"
print(str)

msg = pynmea2.parse(str)
print(msg)
print (f"Timestamp: {msg.timestamp} -- Lat: {msg.lat} {msg.lat_dir} " \
              f"-- Lon: {msg.lon} {msg.lon_dir} -- Altitude:{msg.altitude} {msg.altitude_units}")