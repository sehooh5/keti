from flask import Flask, render_template, Response, request, g, jsonify
from flask_cors import CORS, cross_origin
import json
import sqlite3
import datetime

app = Flask(__name__)
CORS(app)
port = 8088

# DB 생성 (오토 커밋)
conn = sqlite3.connect("tcp_test.db", isolation_level=None, check_same_thread=False)

# 커서 획득
c = conn.cursor()

@app.route('/')
def index():
    return "index"

@app.route('/gps', methods=['POST'])
def gps():
    global json_data
    json_data = request.get_json(silent=True)
    gps_id = json_data['gps_id']
    gps_lat = json_data['gps_lat']
    gps_lat_dir = json_data['gps_lat_dir']
    gps_lon = json_data['gps_lon']
    gps_lon_dir = json_data['gps_lon_dir']
    gps_alt = json_data['gps_alt']
    gps_alt_units = json_data['gps_alt_units']
    gps_time = json_data['gps_time']

    # device table 생성 후 데이터 저장
    c.execute(f'select name from sqlite_master where type="table" and name="{gps_id}"')
    dt_exist = c.fetchone()
    # d_id 테이블이 없으면 테이블 생성
    if dt_exist == None:
        print(f"{gps_id} 테이블 생성")
        c.execute(f"CREATE TABLE IF NOT EXISTS {gps_id} \
                        (id integer PRIMARY KEY, gps_lat text, gps_lat_dir text, gps_lon text, gps_lon_dir text, gps_alt text, gps_alt_units text, gps_time text)")
    c.execute((f"SELECT COUNT(*) from {gps_id}"))
    count = c.fetchall()[0][0]
    if count == 0:
        mid = 1
        # print(type(mid))
    else:
        c.execute(f"SELECT max(id) FROM {gps_id}")
        mid = c.fetchone()[0] + 1  # 가장 큰 id 값

        c.execute(f"SELECT min(id) FROM {gps_id}")
        delete_id = c.fetchone()[0]
        c.execute(f"DELETE FROM {gps_id} WHERE id=?", (delete_id,))
        if mid == 100: # DB에 100번 이상 넘어가면 다시 1으로..
            mid = 1

    c.execute(f"INSERT INTO {gps_id} \
                VALUES(?,?,?,?,?,?,?,?)", (mid, gps_lat, gps_lat_dir, gps_lon, gps_lon_dir, gps_alt, gps_alt_units, gps_time))

    return "GPS data is loaded!"

@app.route('/gps_save', methods=['POST'])
def gps_save():
    global json_data
    json_data = request.get_json(silent=True)
    gps_id = json_data['gps_id']
    gps_lat = json_data['gps_lat']
    gps_lat_dir = json_data['gps_lat_dir']
    gps_lon = json_data['gps_lon']
    gps_lon_dir = json_data['gps_lon_dir']
    gps_alt = json_data['gps_alt']
    gps_alt_units = json_data['gps_alt_units']
    gps_time = json_data['gps_time']

    # gps_id_save table 생성 후 데이터 저장
    c.execute(f'select name from sqlite_master where type="table" and name="{gps_id}_save"')
    dt_exist = c.fetchone()
    # gps_id 테이블이 없으면 테이블 생성
    if dt_exist == None:
        print(f"{gps_id}_save 테이블 생성")
        c.execute(f"CREATE TABLE IF NOT EXISTS {gps_id}_save \
                        (gps_lat text, gps_lat_dir text, gps_lon text, gps_lon_dir text, gps_alt text, gps_alt_units text, gps_time text)")

    c.execute(f"INSERT INTO {gps_id}_save \
                VALUES(?,?,?,?,?,?,?)", (gps_lat, gps_lat_dir, gps_lon, gps_lon_dir, gps_alt, gps_alt_units, gps_time))

    return "GPS data is saved in Edge Server!"


@app.route('/get_gpsData', methods=['GET'])
def get_gpsData():
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

# 0902 // 1초마다 GPS 데이터 읽는 API
@app.route('/gps_temp', methods=['POST'])
def gps_temp():
    global temp_data
    temp_data = request.get_json(silent=True)

    return temp_data

# 0902 // temp data get요청으로 gps json data 리턴
@app.route('/get_gps', methods=['GET'])
def get_gps():
    cid = request.args.get('cid')
    dt = datetime.datetime.utcnow().strftime("%d/%m/%Y, %H:%M:%S")
    if cid == temp_data['cid']:
        print("cid 맞음")

    return temp_data


app.run(host="123.214.186.162",port=port)

