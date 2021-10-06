#!/usr/bin/env python
from models import db, SW_up, Server, Server_SW
from importlib import import_module
import os
from flask import Flask, render_template, Response, request, jsonify
import json
import response
import requests

app = Flask(__name__)


# 2.3 엣지서버에 디바이스 연결
@ app.route('/connect_device', methods=['POST'])
def connect_device():

    json_data = request.get_json(silent=True)
    if json_data == None:
        return response.message("0021")

    eid = json_data['eid']  # 엣지 서버 아이디
    did = json_data['did']  # 디바이스 아이디

    wids = db.session.query(Server_SW.wid).filter(eid == Server_SW.sid).all()
    for wid in wids:
        fname = db.session.query(SW_up.fname).filter(
            SW_up.sid == wid[0]).first()[0]
        if fname == "select_cam":
            sw_id = wid[0]

    nodeport = db.session.query(Server_SW.nodeport).filter(
        Server_SW.sid == eid, Server_SW.wid == sw_id).first()[0]
    print("노드포트 출력 : ", nodeport)

    # 임시로 값 주는중
    d_url = "rtsp://keti:keti1234@192.168.100.60:8805/videoMain"
    data = {
        "url": d_url
    }

    # 나중에 추가
    # requests.post(
    #     f"http://localhost:{nodeport}/connect", data=json.dumps(data))

    return response.message("0000")


# 2.10 마스터/워커 서버에 배포된 SW 목록 조회
@app.route('/get_deploySwList', methods=['POST'])
def get_deploySwList():

    json_data = request.get_json(silent=True)
    print(json_data)
    if json_data == None:
        return response.message("0021")

    sid = json_data['sid']
    sw_list = []

    s = db.session.query(Server_SW.wid).filter(sid == Server_SW.sid).all()
    for sw in s:
        Key = "wid"
        Value = sw[0]
        string = {Key: Value}
        sw_list.append(string)

    res = jsonify(
        code="0000",
        message="처리 성공",
        swList=sw_list
    )
    return res

# 2.6 마스터 서버에 업로드된 소프트웨어 정보 조회


@app.route('/get_uploadSwInfo', methods=['POST'])
def get_uploadSwInfo():

    json_data = request.get_json(silent=True)
    if json_data == None:
        return response.message("0021")

    sid = json_data['sid']

    name = db.session.query(SW_up.name).filter(SW_up.sid == sid).first()[0]
    fname = db.session.query(SW_up.fname).filter(SW_up.sid == sid).first()[0]
    copyright = db.session.query(SW_up.copyright).filter(
        SW_up.sid == sid).first()[0]
    type = db.session.query(SW_up.type).filter(SW_up.sid == sid).first()[0]
    desc = db.session.query(SW_up.description).filter(
        SW_up.sid == sid).first()[0]
    dt = db.session.query(SW_up.datetime).filter(SW_up.sid == sid).first()[0]

    res = jsonify(
        code="0000",
        message="처리 성공",
        name=name,
        fname=fname,
        copyright=copyright,
        type=type,
        description=desc,
        datetime=dt.strftime('%Y-%m-%d')
    )
    return res


# DB관련
# 현재있는 파일의 디렉토리 절대경로
basdir = os.path.abspath(os.path.dirname(__file__))
# basdir 경로안에 DB파일 만들기
dbfile = os.path.join(basdir, 'db.sqlite')

# SQLAlchemy 설정

# 내가 사용 할 DB URI
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///' + dbfile
# 비지니스 로직이 끝날때 Commit 실행(DB반영)
app.config['SQLALCHEMY_COMMIT_ON_TEARDOWN'] = True
# 수정사항에 대한 TRACK
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
# SECRET_KEY
app.config['SECRET_KEY'] = 'jqiowejrojzxcovnklqnweiorjqwoijroi'

db.init_app(app)
db.app = app
db.create_all()

if __name__ == '__main__':
    app.run(host='0.0.0.0', threaded=True, port=5080)
