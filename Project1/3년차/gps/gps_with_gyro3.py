import json
import time



def read_file():
    f = open("test.txt", "r")
    line = f.read()
    json_data = json.loads(line)
    print(json_data)
    f.close
    return json_data

j = read_file()
print(j['gps']['lat_dd'])

## 무한 루프
# while True:
#     i = 0;
#     data = read_file()
#     print(data)
#     time.sleep(0.5)
#     if i == 1:
#         break;
