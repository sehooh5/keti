import sqlite3
import struct
import sys
import textwrap # text 자르기
import time

def data_int(data_hex):
    data_byte = bytes.fromhex(data_hex)
    data_int = int.from_bytes(data_byte, byteorder='big', signed=False)

    return data_int

def filter_junk_data(data_hex):
    start_index = data_hex.find("5550") # "5550"의 시작 인덱스를 찾아서 앞에 정크 데이터 삭제

    if start_index != -1:  # "5550"이 존재하는 경우
        data_hex = data_hex[start_index:]  # "5550"부터의 문자열을 새로운 변수에 할당합니다.

        if len(data_hex) != 220: # data_hex의 길이가 22*10보다 크거나 작을때 220 or 더 작은 숫자, 22의 배수로 처리
            left_hex = (len(data_hex) % 22)
            data_hex = data_hex[:-left_hex]

            if len(data_hex) > 220:
                data_hex = data_hex[:220]

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
        print("")
#         time.sleep(0.5)
        data_len = len(data[0])
        data_hex = data[0].hex()
        chunk_size = 22
        if data_len >= 110 and '5550' in data_hex: # 나중에 전체 507개 데이터 사용할 때 이 부분으로 진행해야함
            cnt+=1
            print(f"count : {cnt}, data_len : {data_len}\n")
            data_hex = filter_junk_data(data_hex) # hex 데이터 55부터 시작 및 길이 맞춰주기
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
                        data_list = data_list[1:]

                        if data_delimiter == '50':
                            print('Time Output')
                            year = data_int(data_list[0])
                            month = data_int(data_list[1])
                            day = data_int(data_list[2])
                            hour = data_int(data_list[3])
                            min = data_int(data_list[4])
                            sec = data_int(data_list[5])
                            ms = (data_int(data_list[7])<<8) | data_int(data_list[6])

                            data_sum = 0
                            for i in range(0,8):
                                data_sum += data_int(data_list[i])
                                print(i, data_int(data_list[i]))

                            print('checksum : ', data_int(data_list[8]), 'data_sum : ', data_sum) # check sum 확인

                            print(f'20{year}/{month}/{day}/{hour}:{min}:{sec}:{ms}\n')

                        elif data_delimiter == '51':
                            print('Acceleration')
                            ax = ((data_int(data_list[1])<<8) | data_int(data_list[0]))/32768*16*9.8
                            ay = ((data_int(data_list[3])<<8) | data_int(data_list[2]))/32768*16*9.8
                            az = ((data_int(data_list[5])<<8) | data_int(data_list[4]))/32768*16*9.8
                            temper = ((data_int(data_list[7])<<8) | data_int(data_list[6]))/100

                            print(f'ax : {ax}, ay : {ay},az : {az},temperature : {temper}\n')
                            
                        elif data_delimiter == '52':
                            print('Angular')
                            wx = ((data_int(data_list[1])<<8) | data_int(data_list[0]))/32768*2000
                            wy = ((data_int(data_list[3])<<8) | data_int(data_list[2]))/32768*2000
                            hdop = ((data_int(data_list[5])<<8) | data_int(data_list[4]))/32768*2000
                            temper = ((data_int(data_list[7])<<8) | data_int(data_list[6]))/100

                            print(f'wx : {wx}, wy : {wy},hdop : {hdop},temperature : {temper}\n')
                            
                        elif data_delimiter == '53':
                            print('Angle')
                            roll = ((data_int(data_list[1])<<8) | data_int(data_list[0]))/32768*180
                            pitch = ((data_int(data_list[3])<<8) | data_int(data_list[2]))/32768*180
                            yaw = ((data_int(data_list[5])<<8) | data_int(data_list[4]))/32768*180
                            version = ((data_int(data_list[7])<<8) | data_int(data_list[6]))

                            print(f'roll : {roll}, pitch : {pitch},yaw : {yaw},version : {version}\n')
                            
                        elif data_delimiter == '54':
                            print('Magnetic')
                            mx = ((data_int(data_list[1])<<8) | data_int(data_list[0]))
                            my = ((data_int(data_list[3])<<8) | data_int(data_list[2]))
                            mz = ((data_int(data_list[5])<<8) | data_int(data_list[4]))
                            temper = ((data_int(data_list[7])<<8) | data_int(data_list[6]))/100

                            print(f'mx : {mx}, my : {my},mz : {mz},temperature : {temper}\n')

                        elif data_delimiter == '56':
                            print('Atmospheric Pressure and Height')
                            press = (data_int(data_list[3])<<24) | (data_int(data_list[2])<<16) | (data_int(data_list[1])<<8) | data_int(data_list[0])
                            h = (data_int(data_list[7])<<24) | (data_int(data_list[6])<<16) |(data_int(data_list[5])<<8) | data_int(data_list[4])

                            print(f'press : {press}, h : {h}\n')
                            
                        elif data_delimiter == '57':
                            print('Longitude and Latitude')
                            lon = (data_int(data_list[3])<<24) | (data_int(data_list[2])<<16) | (data_int(data_list[1])<<8) | data_int(data_list[0])
                            lat = (data_int(data_list[7])<<24) | (data_int(data_list[6])<<16) | (data_int(data_list[5])<<8) | data_int(data_list[4])
                            lon_dd = int(lon/10000000)
                            lat_dd = int(lat/10000000)
                            lon_mm = ((lon/10000000-lon_dd)*100)/60
                            lat_mm = ((lat/10000000-lat_dd)*100)/60
                            lon_final = lon_dd+lon_mm
                            lat_final = lat_dd+lat_mm

                            print(f'lat : {lat_final} / lon : {lon_final}\n')


                            cnt_temp_gps+=1
                        elif data_delimiter == '58':
                            print('Ground Speed')
                            gh = ((data_int(data_list[1])<<8) | data_int(data_list[0]))/10
                            gy = ((data_int(data_list[3])<<8) | data_int(data_list[2]))/10
                            gv = ((data_int(data_list[7])<<24) | (data_int(data_list[6])<<16) |(data_int(data_list[5])<<8) | data_int(data_list[4]))/1000

                            print(f'gh : {gh}, gy : {gy}, gv : {gv}\n')

                        elif data_delimiter == '59':
                            print('Quaternion')
                            q0 = ((data_int(data_list[1])<<8) | data_int(data_list[0]))/32768
                            q1 = ((data_int(data_list[3])<<8) | data_int(data_list[2]))/32768
                            q2 = ((data_int(data_list[5])<<8) | data_int(data_list[4]))/32768
                            q3 = ((data_int(data_list[7])<<8) | data_int(data_list[6]))/32768

                            print(f'q0 : {q0}, q1 : {q1}, q2 : {q2}, q3 : {q3}\n')
                            
                        elif data_delimiter == '5a':
                            print('Satellite Positioning Accuracy')
                            snum = ((data_int(data_list[1])<<8) | data_int(data_list[0]))
                            pdop = ((data_int(data_list[3])<<8) | data_int(data_list[2]))/32768
                            hdop = ((data_int(data_list[5])<<8) | data_int(data_list[4]))/32768
                            vdop = ((data_int(data_list[7])<<8) | data_int(data_list[6]))/32768

                            print(f'snum : {snum}, pdop : {pdop},hdop : {hdop},vdop : {vdop}\n')
                            
                        else:
                            print('Unable Data!')

#     print(cnt_temp_gps) # gps 갯수 카운팅
    conn.close()
    return datas

# 예시 사용
db_num = sys.argv[1]
db_path = f"/home/keti01/keti/Project1/4th/GPSDataCast/gps_0{db_num}.db"
table_name = "gps_raw_data"
column_name = "raw_data"

raw_data = get_data(db_path, table_name, column_name)