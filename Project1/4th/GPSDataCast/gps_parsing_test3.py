import sqlite3
import struct
import sys
import textwrap # text 자르기

def get_data(db_file, table_name, column_name):
    conn = sqlite3.connect(db_file)
    cursor = conn.cursor()

    # 데이터 크기 쿼리 실행
#     query = f"SELECT LENGTH({column_name}) FROM {table_name}"
    query = f"SELECT {column_name} FROM {table_name}"
    cursor.execute(query)

    # 데이터 1개
    data = cursor.fetchone()
    print(data)

    # 데이터 모두 추출
    datas = cursor.fetchall()
    len_data = len(datas)
    cnt = 0
    for data in datas:
        cnt+=1
        print("[[START PRINT]]")
        print(f"count : {cnt}/3242")

        # 데이터 형태가 data[0] 인지 data[0].hex() 인지 모르겠음
        chunk_size = 22
        data_hex = data[0].hex() # 숫자 문자열 형태
        data_bytes = data[0] # 바이트 형태

        print("bytes : ",data_bytes)
        print("hex : ",data_hex)
        print(textwrap.wrap(string, chunk_size))

        print("데이터 길이 : ", len(data[0]))
#         print(data[0].split(b'\\')) # x17/x04...형태
#         print(data[0].decode('ascii'))
        print("[END PRINT]")
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