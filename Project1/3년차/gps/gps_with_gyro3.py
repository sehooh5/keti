import sys
import json
import time
import requests


url = "http://123.214.186.162:8088"

def read_file():
    f = open("test.txt", "r")
    line = f.read()
    # json_data = json.loads(line)

    # lat=json_data['gps']['lat_dd']+json_data['gps']['lat_mm']
    # lon = json_data['gps']['lon_dd'] + json_data['gps']['lon_mm']

    f.close
    return line

## 무한 루프
while True:
    i = 0;
    data = read_file()

    arg = sys.argv
    if len(arg) > 0 :
        res = requests.post(f'{url}/gwg_save', json=data)
    else:
        res = requests.post(f'{url}/gwg', json=data)

    print(res)
    time.sleep(0.5)
    if i == 1:
        break;
