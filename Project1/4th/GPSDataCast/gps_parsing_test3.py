import sqlite3
import struct
import sys

def get_data(db_file, table_name, column_name):
    conn = sqlite3.connect(db_file)
    cursor = conn.cursor()

    # 데이터 크기 쿼리 실행
#     query = f"SELECT LENGTH({column_name}) FROM {table_name}"
    query = f"SELECT {column_name} FROM {table_name}"
    cursor.execute(query)
    data = cursor.fetchone()[0]
    print(data)

    datas = cursor.fetchall()
    len_data = len(datas)

#     for data in datas:
#         # 데이터 형태가 data[0] 인지 data[0].hex() 인지 모르겠음
#         print(data[0].hex())
#         print(data[0])
#         unpacked_data = struct.unpack('III', data[0])
#         print(unpacked_data)

    conn.close()
    return datas

# 예시 사용
db_num = sys.argv[1]
db_file = f"gps_0{db_num}.db"
table_name = "gps_raw_data"
column_name = "raw_data"

raw_data = get_data(db_file, table_name, column_name)
# print(raw_data)
# print(f"데이터: {raw_data}")