import json
import time



def read_file():
    f = open("test.txt", "r")
    line = f.read()
    json_data = json.loads(line)
    lat=json_data['gps']['lat_dd']+json_data['gps']['lat_mm']
    lon = json_data['gps']['lon_dd'] + json_data['gps']['lon_mm']

    f.close
    return json_data

read_file()
# j = read_file()
# print(type(j['gps']['lat_dd']))
# print(type(j['gps']['lat_mm']))

## 무한 루프
# while True:
#     i = 0;
#     data = read_file()
#     print(data)
#     time.sleep(0.5)
#     if i == 1:
#         break;
