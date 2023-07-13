import sqlite3
import struct
import sys
import textwrap # text 자르기
import time

def data_int(data_hex):
    data_byte = bytes.fromhex(data_hex)
    data_int = int.from_bytes(data_byte, byteorder='big', signed=False)
    return data_int

def delete_junk_hex(data_hex):
    # "5550"의 시작 인덱스를 찾아서 앞에 정크 데이터 삭제
    start_index = data_hex.find("5550")
    if start_index != -1:  # "5550"이 존재하는 경우
        data_hex = data_hex[start_index:]  # "5550"부터의 문자열을 새로운 변수에 할당합니다.
    else:
        data_hex = data_hex
    return data_hex

def get_data(db_path, table_name, column_name):
    conn = sqlite3.connect(db_path)
    cursor = conn.cursor()
    query = f"SELECT {column_name} FROM {table_name}"
    cursor.execute(query)

    # 데이터 모두 추출
    datas = cursor.fetchall()
    len_data = len(datas)
    cnt = 0
    cnt_temp_gps = 0 # gps 갯수 카운팅
    for data in datas:
        data_len = len(data[0])
        chunk_size = 22
        if data_len >= 10: # 나중에 전체 507개 데이터 사용할 때 이 부분으로 진행해야함
#         if data_len >= 110 | data_len <= 140: # 2개 데이터, 59 까지 사용 가능
            cnt+=1
            print(f"count : {cnt}, data_len : {data_len}")
            data_hex = data[0].hex() # 숫자 문자열 형태
            data_hex = delete_junk_hex(data_hex)
            data_hex_list = textwrap.wrap(data_hex, chunk_size)


            print(data_hex)
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
                            cnt_temp_gps+=1
                        elif data_delimiter == '58':
                            print('Ground Speed')
                            
                        elif data_delimiter == '59':
                            print('Quaternion')
                            
                        elif data_delimiter == '5a':
                            print('0 Satellite Positioning Accuracy')
                            
                        else:
                            print('Unable Data!')
    time.sleep(0.5)

#     print(cnt_temp_gps) # gps 갯수 카운팅
    conn.close()
    return datas

# 예시 사용
db_num = sys.argv[1]
db_path = f"/home/keti01/keti/Project1/4th/GPSDataCast/gps_0{db_num}.db"
table_name = "gps_raw_data"
column_name = "raw_data"

raw_data = get_data(db_path, table_name, column_name)