import requests
import sqlite3
import time
import os
import sys

# num = sys.argv[1]

# conn = sqlite3.connect(f"gps_0{num}.db", isolation_level=None, check_same_thread=False)
# c = conn.cursor()
#
# c.execute("SELECT COUNT(*) FROM gps_raw_data")
# for row in c:
#     num = row[0]
# print(num)
#
# # "bid": row[0],
# # "time": row[1],
# # "gps_raw_data": row[2]
# while True:
#     for num in range(1, num+1):
#         if num == 1:
#             print("데이터 초기화")
#         c.execute(f"SELECT * FROM gps_raw_data WHERE ROWID={num}")
#         for row in c:
# #             decoded_data = bytes.fromhex(row[2])
#             print(f"로우 데이터 {row[0]}: {row[2]}")
#
#
#
#         time.sleep(0.5)

# url = 'http://123.214.186.162:8089/get_gps_rdata'
# bid = f'bb0{num}'
# params = {
#     'bid': bid
# }
# while True:
#     res = requests.get(url, params)
#     raw_data = res.json()['gps_raw_data']
#
#     print(raw_data)
#
#     time.sleep(0.5)


def parse_data(raw_data):
    data_length = len(raw_data)
    index = 0

    while index < data_length:
        # 첫 번째 바이트를 확인하여 데이터 형식을 결정합니다.
        marker = raw_data[index]
        index += 1

        if marker != 0x55:
            print(f"Error: Invalid marker byte {hex(marker)}")
            continue

        # 두 번째 바이트를 확인하여 데이터 형식을 결정합니다.
        data_type = raw_data[index]
        index += 1

        # 데이터 형식에 따라 파싱하여 처리합니다.
        if data_type == 0x50:
            # 데이터 형식 0x50 처리 (예: ...)
            pass
        elif data_type == 0x51:
            # 데이터 형식 0x51 처리 (예: ...)
            pass
        elif data_type == 0x52:
            # 데이터 형식 0x52 처리 (예: ...)
            pass
        elif data_type == 0x53:
            # 데이터 형식 0x53 처리 (예: ...)
            pass
        elif data_type == 0x54:
            # 데이터 형식 0x54 처리 (예: ...)
            pass
        else:
            print(f"Error: Unknown data type {hex(data_type)}")

# 데이터베이스에서 raw 데이터를 가져옵니다. (여기에서는 가정하고 진행합니다)
raw_data = b'\x55\x50\x01\x02\x55\x51\x03\x04\x55\x52\x05\x06\x55\x53\x07\x08\x55\x54\x09\x0A'

parse_data(raw_data)