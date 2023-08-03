from flask import Flask, render_template, Response, request, g, jsonify
from flask_cors import CORS, cross_origin
import json
import sqlite3
import datetime
import sys
import time

app = Flask(__name__)
CORS(app)
port = 8090

bnum = sys.argv[1]
conn = sqlite3.connect("gwg_test_SA_1.db", isolation_level=None, check_same_thread=False)
c = conn.cursor()

c.execute(f"SELECT lat, lon FROM gps_0{bnum}")
rows = c.fetchall()
global lat
global lon

# for row in rows:
#     lat, lon = row
#     time.sleep(0.5)

@app.route('/')
def index():
    json_data = request.get_json(silent=True)
    print(json_data)
    return "index"

@app.route('/get_gps_data', methods=['GET'])
def get_gps_data():
    global lat
    global lon

    data = {
    "code": "0000",
    "message": "처리 성공",
    "lat": lat,
    "lon": lon,
    }
    json_data = json.dumps(data)

    return json_data

app.run(host="123.214.186.162",port=port)