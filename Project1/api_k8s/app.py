#!/usr/bin/env python
from importlib import import_module
from flask import Flask, render_template, Response, request, jsonify
import os
from models import db, SW_up, Server, Server_SW
import datetime as dt
import string 
import random


app = Flask(__name__)
app.config['JSON_AS_ASCII'] = False # jsonify 한글깨짐 해결

# 랜덤한 문자열 생성 
_LENGTH = 4 # 12자리 # 숫자 + 대소문자 
string_pool = string.ascii_letters + string.digits 
def sid_maker():
    sid = ""    
    for i in range(_LENGTH) :
        sid += random.choice(string_pool) 
    return sid

def port_maker(len):
    port = ""    
    for i in range(len) :
        port += random.choice(string.digits) 
    return port

@app.route('/')
def index():
  
    return render_template('api_k8s.html')

# 2.1 신규 엣지 클러스터 추가 
## get_edgeInfo 사용
@app.route('/add_newEdgeCluster', methods=['POST'])
def add_newEdgeCluster():
    mid = request.form['mid']
    wlist = request.form['wlist'] # list 로 받아서 여러개의 id 를 가져오거나 보내야 할수도잇음
    # ### 일단 기능은 빼고 껍데기만 만들어 놓기 --->
    # # 마스터 엣지 ip 불러오기
    # mip = get_edgeInfo(mid).ip
    # # 마스터 엣지 구성
    # m_output = os.system(f"sudo kubeadm init --pod-network-cidr=10.244.0.0/16 --apiserver-advertise-address={mip}")
    # # 워커 엣지에서 사용할 코드
    # w_input = m_message.split('root:')[-1]
    # ### 여기서 wlist 로 wid 가져와서 원격으로 접속한 뒤 w_input 입력해주기? ###

    
    # 응답부분
    res = jsonify(
        code = "0000",
        message = "처리 성공"
    )
    return res

# 엣지 서버들 이름 조회
@app.route('/get_edgeName', methods=['GET'])
def get_edgeName():
    nodes = os.system(f"kubectl get node")
    nodes_split = s.split('\n')
    len_nodes = len(nodes_split)

    name_list = nodes_split[1:len_nodes] 
    names = []
    for name in node_list:
        n = {"name" : name.split(' ')[0]}
        names.append(n)

    # 응답부분
    res = jsonify(
        code = "0000",
        message = "처리 성공",
        nlist = names
    )
    return res

# 2.3 엣지서버에 디바이스 연결
@app.route('/connect_device', methods=['POST'])
def connect_device():
    eid = request.form['eid']
    did = request.form['eid']
    
    # 응답부분
    res = jsonify(
        code = "0000",
        message = "처리 성공"
    )
    return res

# 2.4 엣지서버에 연결된 디바이스 연결 해지
@app.route('/disconnect_device', methods=['POST'])
def disconnect_device():
    eid = request.form['eid']
    did = request.form['did']
    
    # 응답부분
    res = jsonify(
        code = "0000",
        message = "처리 성공"
    )
    return res

# 2.5 마스터 서버가 저장하고 있는 업로드 소프트웨어 목록 조회
@app.route('/get_uploadSwList', methods=['GET'])
def get_uploadSwList():

    sid_list = db.session.query(SW_up.sid).all()
    name_list = db.session.query(SW_up.name).all()
    fname_list = db.session.query(SW_up.fname).all()
    copyright_list = db.session.query(SW_up.copyright).all()
    type_list = db.session.query(SW_up.type).all()
    desc_list = db.session.query(SW_up.description).all()
    dt_list = db.session.query(SW_up.datetime).all()
    
    sw_list = []
    for sid, name, fname, copyright, type, desc, datetime in zip(sid_list, name_list, fname_list, copyright_list, type_list, desc_list, dt_list): 
        dt = datetime[0].strftime('%Y-%m-%d')
        sw = {
        "sid" : sid[0],
        "name": name[0],
        "fname": fname[0],
        "copyright": copyright[0],
        "type": type[0],
        "description": desc[0],
        "datetime": dt
        }
        sw_list.append(sw)
        


    # 응답부분 (List 구현해야함)
    res = jsonify(
        code = "0000",
        message = "처리 성공",
        list = sw_list
    )
    return res

# 2.6 마스터 서버에 업로드된 소프트웨어 정보 조회
@app.route('/get_uploadSwiNFO', methods=['POST'])
def get_uploadSwiNFO():
    sid = request.form['sid']

    name = db.session.query(SW_up.name).filter(SW_up.sid == sid).first()[0]
    fname = db.session.query(SW_up.fname).filter(SW_up.sid == sid).first()[0]
    copyright = db.session.query(SW_up.copyright).filter(SW_up.sid == sid).first()[0]
    type = db.session.query(SW_up.type).filter(SW_up.sid == sid).first()[0]
    desc = db.session.query(SW_up.description).filter(SW_up.sid == sid).first()[0]
    dt = db.session.query(SW_up.datetime).filter(SW_up.sid == sid).first()[0]


    # 응답부분 (List 구현해야함)
    res = jsonify(
        code = "0000",
        message = "처리 성공",
        name = name,
        fname = fname,
        copyright = copyright,
        type = type,
        description = desc,
        datetime = dt.strftime('%Y-%m-%d')
    )
    return res

# 2.7 마스터 서버에 업로드한 신규 소프트웨어 등록
@app.route('/add_newUploadSw', methods=['POST'])
def add_newUploadSw():
    name = request.form['name']
    fname = request.form['fname']
    copyright = request.form['copyright']
    type = request.form['type']
    desc = request.form['desc']
    
    # 1. sid 생성
    sid = sid_maker()
    q = db.session.query(SW_up).get(sid) # sid 중복된게 있는지 찾아줌

    while q != None :
        print("sid 생성")
        sid = sid_maker()
        break
    else :
        print(f"using {sid}")
    
    # 2. software_up 테이블에 데이터 저장
    sw = SW_up(sid=sid, name=name, fname=fname, copyright=copyright, type=type, description=desc)    
    db.session.add(sw)
    db.session.commit

    # 응답부분
    res = jsonify(
        code = "0000",
        message = "처리 성공",
        sid = sid
    )
    return res


# 2.8 마스터 서버에 업로드된 SW 정보수정
@app.route('/update_uploadSw', methods=['POST'])
def update_uploadSw():
    sid = request.form['sid']
    name = request.form['name']
    fname = request.form['fname']
    copyright = request.form['copyright']
    type = request.form['type']    
    desc = request.form['desc']

    
    sw = db.session.query(SW_up).filter(SW_up.sid == sid).update({
         'sid': sid,
         'name': name,
         'fname': fname,
         'copyright': copyright,
         'type': type,
         'description': desc
         })
    db.session.commit()

    # 응답부분
    res = jsonify(
        code = "0000",
        message = "처리 성공"
    )
    return res


# 2.9 마스터 서버에 업로드된 SW 삭제
@app.route('/remove_uploadSw', methods=['POST'])
def remove_uploadSw():
    sid = request.form['sid']
    print(sid)
    sw = db.session.query(SW_up).filter(SW_up.sid == sid).first()
    print(sw)
    db.session.delete(sw)
    db.session.commit()

    # 응답부분
    res = jsonify(
        code = "0000",
        message = "처리 성공"
    )
    return res

# 2.10 마스터/워커 서버에 배포된 SW 목록 조회
@app.route('/get_deploySwList', methods=['POST'])
def get_deploySwList():
    sid = request.form['sid'] # 일단 이렇게 진행하는데 왜 sid인지?
    sw_list = []

    s = db.session.query(Server_SW.wid).filter(sid == Server_SW.sid).all() 
    for sw in s:
        Key = "wid"
        Value = sw[0]
        string = {Key : Value}
        sw_list.append(string)
        

    # 응답부분 (List 구현해야함)
    res = jsonify(
        code = "0000",
        message = "처리 성공",
        swList = sw_list
    )
    return res

# 2.11 마스터/워커 서버에 배포된 SW 정보 등록
@app.route('/add_newDeploySwInfo', methods=['POST'])
def add_newDeploySwInfo():
    sid = request.form['sid']
    wid = request.form['wid']
    
    # server data 임의로 넣어주고잇음
#    ser = Server(sid = "master1")
#    db.session.add(ser)
#    db.session.commit

    s = Server_SW(sid = sid, wid = wid)
    db.session.add(s)
    db.session.commit

    # 응답부분 
    res = jsonify(
        code = "0000",
        message = "처리 성공"
    )
    return res

# 2.12 마스터/워커 서버에 배포된 SW 삭제
@app.route('/remove_deploySwInfo', methods=['POST'])
def remove_deploySwInfo():
    sid = request.form['sid']
    wid = request.form['wid']

    sw = db.session.query(Server_SW).filter(Server_SW.sid == sid, Server_SW.wid == wid).first()
    print(sw)
    db.session.delete(sw)
    db.session.commit()

    # 응답부분 
    res = jsonify(
        code = "0000",
        message = "처리 성공"
    )
    return res

# 2.13 마스터 서버의 사용 가능한 서비스 포트 조회
@app.route('/get_servicePort', methods=['POST'])
def get_servicePort():
    sid = request.form['sid']

    p_list = db.session.query(Server_SW.serviceport).filter(Server_SW.sid == sid).all()
    port_list = []
    for p in p_list:
        port = p[0]
        port_list.append(port)
    
    port = f"6{port_maker(3)}"
    while True:
        if port in port_list:
            port = f"6{port_maker(3)}"
            print(f"해당 포트번호는 사용중입니다. 포트번호를 재생성합니다 : {port}")
        else : 
            print(f"해당 포트번호 사용 : {port}")
            break

    # 응답부분 
    res = jsonify(
        code = "0000",
        message = "처리 성공",
        port = port
    )
    return res

# 2.14 마스터 서버의 사용 가능한 타깃 포트 조회
@app.route('/get_targetPort', methods=['POST'])
def get_targetPort():
    sid = request.form['sid']

    p_list = db.session.query(Server_SW.targetport).filter(Server_SW.sid == sid).all()
    port_list = []
    for p in p_list:
        port = p[0]
        port_list.append(port)
    
    port = f"5{port_maker(3)}"
    while True:
        if port in port_list:
            port = f"5{port_maker(3)}"
            print(f"해당 포트번호는 사용중입니다. 포트번호를 재생성합니다 : {port}")
        else : 
            print(f"해당 포트번호 사용 : {port}")
            break

    # 응답부분 
    res = jsonify(
        code = "0000",
        message = "처리 성공",
        port = port
    )
    return res

# 2.15 마스터 서버의 사용 가능한 노드 포트 조회
@app.route('/get_nodePort', methods=['POST'])
def get_nodePort():
    sid = request.form['sid']

    p_list = db.session.query(Server_SW.nodeport).filter(Server_SW.sid == sid).all()
    port_list = []
    for p in p_list:
        port = p[0]
        port_list.append(port)
        
    port = f"3{port_maker(4)}"
    while True:
        if port in port_list:
            port = f"3{port_maker(4)}"
            print(f"해당 포트번호는 사용중입니다. 포트번호를 재생성합니다 : {port}")
        else : 
            print(f"해당 포트번호 사용 : {port}")
            break

    # 응답부분 
    res = jsonify(
        code = "0000",
        message = "처리 성공",
        port = port
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
    app.run()
