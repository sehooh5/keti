from flask import Flask, render_template, Response, request, g, jsonify
from flask_cors import CORS, cross_origin
import json
import sqlite3
import datetime

app = Flask(__name__)
CORS(app)
port = 8088

# DB 생성 (오토 커밋)
conn = sqlite3.connect("gwg_test_SA_1.db", isolation_level=None, check_same_thread=False)

# 커서 획득
c = conn.cursor()

@app.route('/')
def index():
    json_data = request.get_json(silent=True)
    print(json_data)
    return "index"

@app.route('/gwg', methods=['POST'])
def gwg():
    data = request.get_json(silent=True)
    global gwg_data
    gwg_data = json.loads(data)

    # 50 time
    yy, mm, dd, hh, mi, ss, ms = gwg_data['time']['yy'], gwg_data['time']['mm'], gwg_data['time']['dd'], gwg_data['time']['hh'], gwg_data['time']['mi'], gwg_data['time']['ss'], gwg_data['time']['ms']
    # 51 acceleration
    ax, ay, az = round(gwg_data['acc']['ax'],6), round(gwg_data['acc']['ay'],6), round(gwg_data['acc']['az'],6)
    # 52 angular
    wx, wy, wz = gwg_data['angular']['wx'], gwg_data['angular']['wy'], gwg_data['angular']['wz']
    # 53 angle
    roll, pitch, yaw = round(gwg_data['angle']['roll'],6), round(gwg_data['angle']['pitch'],6), round(gwg_data['angle']['yaw'],6)
    # 54 magnetic
    mx, my, mz = gwg_data['magnetic']['mx'], gwg_data['magnetic']['my'], gwg_data['magnetic']['mz']
    # 56 atmospheric
    press, h = gwg_data['atmospheric']['press'], gwg_data['atmospheric']['h']
    # 57 gps
    lat, lon = round(gwg_data['gps']['lat_dd'] + gwg_data['gps']['lat_mm'], 6), round(gwg_data['gps']['lon_dd'] + gwg_data['gps']['lon_mm'], 6)
    # 58 groundSpeed
    gh, gy, gv = gwg_data['groundSpeed']['gh'], gwg_data['groundSpeed']['gy'], gwg_data['groundSpeed']['gv']
    # 59 quaternion
    q0, q1, q2, q3 = round(gwg_data['quaternion']['q0'],6), round(gwg_data['quaternion']['q1'],6), round(gwg_data['quaternion']['q2'],6), round(gwg_data['quaternion']['q3'],6)
    # 5a satelite
    snum, pdop, hdop, vdop = gwg_data['satelite']['snum'], gwg_data['satelite']['pdop'], gwg_data['satelite']['hdop'], gwg_data['satelite']['vdop']


    print(f"[DATA PRINT OUT]\n"
          f"yy : {yy}, mm : {mm},dd : {dd},hh : {hh},mi : {mi},ss : {ss},ms : {ms}\n"
          f"ax : {ax}, ay : {ay}, az : {ay}\n"
          f"wx : {wx}, wy : {wy}, wz : {wy}\n"
          f"roll : {roll}, pitch : {pitch}, yaw : {yaw}\n"
          f"mx : {mx}, my : {my}, mz : {my}\n"
          f"press : {press}, h : {h}\n"
          f"lon : {lon}, lat : {lat}\n"
          f"gh : {gh}, gy : {gy}, gv : {gv}\n"
          f"q0 : {q0}, q1 : {q1}, q2 : {q2}, q3 : {q3}\n"
          f"snum : {snum}, pdop : {pdop}, hdop : {hdop}, vdop : {vdop}\n")

    return "GPS and Gyro data loaded!!"


@app.route('/gwg_save', methods=['POST'])
def gwg_save():
    data = request.get_json(silent=True)
    global gwg_data
    gwg_data = json.loads(data)

    # gwg data 데이터 추출해서 변수에 저장
    yy, mm, dd, hh, mi, ss, ms = gwg_data['time']['yy'], gwg_data['time']['mm'], gwg_data['time']['dd'], gwg_data['time']['hh'], gwg_data['time']['mi'], gwg_data['time']['ss'], gwg_data['time']['ms']
    ax, ay, az = gwg_data['acc']['ax'], gwg_data['acc']['ay'], gwg_data['acc']['az']
    wx, wy, wz = gwg_data['angular']['wx'], gwg_data['angular']['wy'], gwg_data['angular']['wz']
    roll, pitch, yaw = gwg_data['angle']['roll'], gwg_data['angle']['pitch'], gwg_data['angle']['yaw']
    mx, my, mz = gwg_data['magnetic']['mx'], gwg_data['magnetic']['my'], gwg_data['magnetic']['mz']
    press, h = gwg_data['atmospheric']['press'], gwg_data['atmospheric']['h']
    lat, lon = round(gwg_data['gps']['lat_dd'] + gwg_data['gps']['lat_mm'], 6), round(gwg_data['gps']['lon_dd'] + gwg_data['gps']['lon_mm'], 6)
    gh, gy, gv = gwg_data['groundSpeed']['gh'], gwg_data['groundSpeed']['gy'], gwg_data['groundSpeed']['gv']
    q0, q1, q2, q3 = gwg_data['quaternion']['q0'], gwg_data['quaternion']['q1'], gwg_data['quaternion']['q2'], gwg_data['quaternion']['q3']
    snum, pdop, hdop, vdop = gwg_data['satelite']['snum'], gwg_data['satelite']['pdop'], gwg_data['satelite']['hdop'], gwg_data['satelite']['vdop']

    # gwg_save table 생성 후 데이터 저장 - 여기선 gps_id 관계없이 그냥 단일 gwg_save 테이블에 저장
    c.execute(f'select name from sqlite_master where type="table" and name="gwg_save"')
    dt_exist = c.fetchone()
    # gwg_save 테이블이 없으면 테이블 생성
    if dt_exist == None:
        print(f"gwg_save 테이블 생성")
        c.execute(f"CREATE TABLE IF NOT EXISTS gwg_save \
                        (yy int, mm int, dd int,hh int,mi int,ss int,ms int,\
                        ax real, ay real, az real,\
                        wx int, wy int, wz int,\
                        roll real, pitch real, yaw real,\
                        mx real, my real, mz real,\
                        press real, h real,\
                        lon real, lat real,\
                        gh real, gy real, gv real,\
                        q0 real, q1 real, q2 real, q3 real,\
                        snum int, pdop float, hdop float, vdop float)")
#34
    c.execute(f"INSERT INTO gwg_save \
                VALUES(?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?)", (yy, mm, dd, hh, mi, ss, ms, ax, ay, az, wx, wy, wz, roll, pitch, yaw, mx, my, mz, press, h, lon, lat, gh, gy, gv, q0, q1, q2, q3, snum, pdop, hdop, vdop))

    return "GPS and Gyro data is saved in Edge Server!"


@app.route('/get_gwgData', methods=['GET'])
def get_gwgData():
    global gwg_data
    j_data = json.dumps(gwg_data)

    return j_data

## 저장된 데이터로 진행하는 내용
# 1124 // 1초마다 GPS client 에서 데이터송되는 API
@app.route('/gwg_temp', methods=['POST'])
def gwg_temp():
    global temp_data
    temp_data = request.get_json(silent=True)

    return temp_data

# 1124 // temp data get요청으로 gwg json data 리턴
@app.route('/get_gwg', methods=['GET'])
def get_gwg():
    global temp_data
    j_data = json.dumps(temp_data)

    return j_data


app.run(host="123.214.186.162",port=port)

