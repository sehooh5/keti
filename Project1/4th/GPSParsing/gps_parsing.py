import sqlite3
import struct
import sys
import textwrap # text 자르기
import time

def data_int(data_hex):
    data_byte = bytes.fromhex(data_hex)
    data_int = int.from_bytes(data_byte, byteorder='big', signed=False)
    return data_int

def get_data(db_path, table_name, column_name):
    print(db_path)
    conn = sqlite3.connect(db_path)
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
        data_len = len(data[0])
        chunk_size = 22
        if data_len >= 10: # 나중에 전체 507개 데이터 사용할 때 이 부분으로 진행해야함
#         if data_len >= 110 | data_len <= 140: # 2개 데이터, 59 까지 사용 가능
            cnt+=1
            print(f"count : {cnt}, data_len : {data_len}")
            data_hex = data[0].hex() # 숫자 문자열 형태
            data_hex_list = textwrap.wrap(data_hex, chunk_size)

            for data_hex_one in data_hex_list:
                dho_list = textwrap.wrap(data_hex_one, 2)

                for dho_one in dho_list:
                    if dho_one == '55':
                        data_list = []
                    else:
                        data_list.append(dho_one)

                    if len(data_list) == 10:
                        data_delimiter = data_list[0]
                        data_list = data_list[1:-1]
                        if data_delimiter == '50':
                            print('Time Output')
                            year = data_int(data_list[0])
                            month = data_int(data_list[1])
                            day = data_int(data_list[2])
                            hour = data_int(data_list[3])
                            min = data_int(data_list[4])
                            sec = data_int(data_list[5])
                            ms = (data_int(data_list[6])<<8) | data_int(data_list[7])
                            print(year, month, day, hour, min, sec, ms)
#                             for data_one in data_list:
#                                 data_cnt += 1
#                                 data_one_byte = bytes.fromhex(data_one)
#                                 value = int.from_bytes(data_one_byte, byteorder='big', signed=False)
#                                 print(value)
                            
                        elif data_delimiter == '51':
                            print('Acceleration')
                            
                        elif data_delimiter == '52':
                            print('Angular')
                            
                        elif data_delimiter == '53':
                            print('Angle')
                            
                        elif data_delimiter == '54':
                            print('Magnetic')
                            
                        elif data_delimiter == '56':
                            print('Atmospheric Pressure and Height')
                            
                        elif data_delimiter == '57':
                            print('Longitude and Latitude')
                            
                        elif data_delimiter == '58':
                            print('Ground Speed')
                            
                        elif data_delimiter == '59':
                            print('Quaternion')
                            
                        elif data_delimiter == '5a':
                            print('0 Satellite Positioning Accuracy')
                            
                        else:
                            print('Unable Data!')
        time.sleep(0.5)



#                     data_byte = bytes.fromhex(dho_one) # 1개 정보에 대한 데이터 내 바이트 1개에 대한 데이터
#                     print(data_byte)


#         print("hex : ",data_hex)
#         print(textwrap.wrap(data_hex, chunk_size))
#         data_bytes = data[0] # 바이트 형태
#         print("bytes : ",data_bytes)
#         print(data[0].split(b'\\')) # x17/x04...형태
#         print(data[0].decode('ascii'))
#         print("[END PRINT]")


    conn.close()
    return datas

# 예시 사용
db_num = sys.argv[1]
db_path = f"/home/keti01/keti/Project1/4th/GPSDataCast/gps_0{db_num}.db"
table_name = "gps_raw_data"
column_name = "raw_data"

raw_data = get_data(db_path, table_name, column_name)
# print(raw_data)
# print(f"데이터: {raw_data}")