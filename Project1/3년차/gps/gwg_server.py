from flask import Flask, render_template, Response, request, g, jsonify
from flask_cors import CORS, cross_origin
import json
import sqlite3
import datetime

app = Flask(__name__)
CORS(app)
port = 8088

# DB 생성 (오토 커밋)
conn = sqlite3.connect("gwg_test.db", isolation_level=None, check_same_thread=False)

# 커서 획득
c = conn.cursor()

@app.route('/')
def index():
    json_data = request.get_json(silent=True)
    return "index"

@app.route('/gwg', methods=['POST'])
def gwg():
    data = request.get_json(silent=True)
    global gwg_data
    gwg_data = json.loads(data)

    yy = gwg_data['time']['yy'], mm = gwg_data['time']['mm'], dd = gwg_data['time']['dd'], hh = gwg_data['time']['hh'], mi = gwg_data['time']['mi'], ss = gwg_data['time']['ss'], ms = gwg_data['time']['ms']
    print(yy,mm,dd,hh,mi,ss,ms)
    lon = round(gwg_data['gps']['lon_dd'] + gwg_data['gps']['lon_mm'], 6)
    lat = round(gwg_data['gps']['lat_dd'] + gwg_data['gps']['lat_mm'], 6)

    print(f"lon : {lon}, lat : {lat}")
    return "GPS and Gyro data loaded!!"


@app.route('/gwg_save', methods=['POST'])
def gwg_save():
    data = request.get_json(silent=True)
    global gwg_data
    gwg_data = json.loads(data)

    # gwg data 데이터 추출해서 변수에 저장
    # gps_lat = json_data['gps_lat']
    # gps_lat_dir = json_data['gps_lat_dir']
    # gps_lon = json_data['gps_lon']
    # gps_lon_dir = json_data['gps_lon_dir']
    # gps_alt = json_data['gps_alt']
    # gps_alt_units = json_data['gps_alt_units']
    # gps_time = json_data['gps_time']

    # gwg_save table 생성 후 데이터 저장 - 여기선 gps_id 관계없이 그냥 단일 gwg_save 테이블에 저장
    c.execute(f'select name from sqlite_master where type="table" and name="gwg_save"')
    dt_exist = c.fetchone()
    # gwg_save 테이블이 없으면 테이블 생성
    if dt_exist == None:
        print(f"gwg_save 테이블 생성")
        c.execute(f"CREATE TABLE IF NOT EXISTS gwg_save \
                        (gps_lat text, gps_lat_dir text, gps_lon text, gps_lon_dir text, gps_alt text, gps_alt_units text, gps_time text)")

    c.execute(f"INSERT INTO gwg_save_save \
                VALUES(?,?,?,?,?,?,?)", (gps_lat, gps_lat_dir, gps_lon, gps_lon_dir, gps_alt, gps_alt_units, gps_time))

    return "GPS and Gyro data is saved in Edge Server!"


@app.route('/get_gwgData', methods=['GET'])
def get_gwgData():
    did = request.args.get('did')
    
    # id 바꿔야함
    c.execute(f"SELECT max(id) FROM {did}_save")
    mid = c.fetchone()[0]
    if mid == None:
        msg="None"
        return msg
    else:
        c.execute(f"SELECT * FROM {did} WHERE id={mid}")
        for row in c:
            data = {
                "lat" : row[1],
                "lat_dir": row[2],
                "lon": row[3],
                "lon_dir": row[4],
                "alt": row[5],
                "alt_units": row[6],
                "dt": row[7]
            }
            json_data = json.dumps(data)

        return json_data

# # 0902 // 1초마다 GPS client 에서 데이터송되는 API
# @app.route('/gps_temp', methods=['POST'])
# def gps_temp():
#     global temp_data
#     temp_data = request.get_json(silent=True)
#
#     return temp_data
#
# # 0902 // temp data get요청으로 gps json data 리턴
# @app.route('/get_gps', methods=['GET'])
# def get_gps():
#     cid = request.args.get('cid')
#     dt = datetime.datetime.utcnow().strftime("%d/%m/%Y, %H:%M:%S")
#
#     if cid == temp_data['cid']:
#         code = "0000"
#         message = "처리 성공"
#         data = {
#             "code": code,
#             "message": message,
#             "cid": temp_data['cid'],
#             "dt": dt,
#             "gps": {
#                 "lat": temp_data['gps']['lat'],
#                 "lat_dir": temp_data['gps']['lat_dir'],
#                 "long": temp_data['gps']['lon'],
#                 "long_dir": temp_data['gps']['lon_dir'],
#                 "alt": temp_data['gps']['alt'],
#                 "alt_units": temp_data['gps']['alt_units'],
#             },
#         }
#     elif cid != temp_data['cid']:
#         code = "0003"
#         message = "ID 오류"
#         data = {
#             "code": code,
#             "message": message,
#         }
#     else:
#         code = "9999"
#         message = "기타 오류"
#         data = {
#             "code": code,
#             "message": message,
#         }
#     print(data)
#     json_data = json.dumps(data)
#
#     return json_data


app.run(host="123.214.186.162",port=port)

