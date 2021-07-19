#!/usr/bin/env python
from importlib import import_module
from flask import Flask, render_template, Response, request, jsonify
import os
from models import db

app = Flask(__name__)
app.config['JSON_AS_ASCII'] = False # jsonify 한글깨짐 해결


@app.route('/')
def index():
    return render_template('api_k8s.html')

# 2.1 신규 엣지 클러스터 추가 
## get_edgeInfo 사용
@app.route('/add_newEdgeCluster', methods=['POST'])
def add_newEdgeCluster():
    mid = request.form['mid']
    wlist = request.form['wlist'] # list 로 받아서 여러개의 id 를 가져오거나 보내야 할수도잇음
    mip = get_edgeInfo(mid).ip
    # 마스터 엣지 구성
    m_output = os.system(f"sudo kubeadm init --pod-network-cidr=10.244.0.0/16 --apiserver-advertise-address={mip}")
    # 워커 엣지에서 사용할 코드
    w_input = m_message.split('root:')[-1]
    ### 여기서 wlist 로 wid 가져와서 원격으로 접속한 뒤 w_input 입력해주기? ###

    
    # 응답부분
    res = jsonify(
        code = "0000",
        message = "처리 성공"
    )
    return res


@app.route('/get_edgeName', methods=['GET'])
def get_edgeName():
    if request.method == 'POST':
        file = request.form['file']
        folder_name = request.form['folder']
        file_name = request.form['fileName']

        # file 작성부분
        f = open(os.getcwd().replace(
            "manager", f'{folder_name}/{file_name}'), 'w')
        f.write(file)
        f.close()
    return render_template('apply_doc.html')


@app.route('/apply', methods=['GET', 'POST'])
def apply():

    if request.method == 'POST':
        file_name = request.form['fileName']
        folder_name = request.form['folder']

        if folder_name == 'manager':
            os.chdir("/home/keti0/keti/Project1-1/REST_API/manager")
            os.system(f"kubectl apply -f {file_name}")
        else:
            os.chdir("/home/keti0/keti/Project1-1/REST_API/viewer")
            os.system(f"kubectl apply -f {file_name}")
        os.chdir("/home/keti0/keti/Project1-1/REST_API/manager")
        os.system("echo %s" % file_name)

    return render_template('apply_doc.html')


@ app.route('/signin', methods=['POST'])
def signin():

    pass

    return render_template('docker_login.html')


@ app.route('/login', methods=['POST'])
def login():

    docker_id = request.form['docker_id']
    docker_pwd = request.form['docker_pwd']
    os.system(f"docker login -u {docker_id} -p {docker_pwd}")

    return render_template('apply_doc.html')


@ app.route('/logout', methods=['POST'])
def logout():

    os.system("docker logout")

    return render_template('apply_doc.html')


@ app.route('/build', methods=['GET', 'POST'])
def build():
    print("========= docker build start =========")

    if request.method == 'POST':
        folder_name = request.form['folder']
        file_name = request.form['fileName']
        docker_name = request.form['dockerName']

        if folder_name == 'manager':
            os.chdir("/home/keti0/keti/Project1-1/REST_API/manager")
            os.system(
                f"docker build -f {file_name} -t sehooh5/{docker_name}:latest {path}")
        else:
            os.chdir("/home/keti0/keti/Project1-1/REST_API/viewer")
            os.system(
                f"docker build -f {file_name} -t sehooh5/{docker_name}:latest {path}")
        os.chdir("/home/keti0/keti/Project1-1/REST_API/manager")

    print("========= docker build success =========")
    return render_template('apply_doc.html')


@ app.route('/push', methods=['GET', 'POST'])
def push():

    folder_name = request.form['folder']
    docker_name = request.form['dockerName']

    if folder_name == 'manager':
        os.chdir("/home/keti0/keti/Project1-1/REST_API/manager")
        os.system(f"docker push sehooh5/{docker_name}:latest")
    else:
        os.chdir("/home/keti0/keti/Project1-1/REST_API/viewer")
        os.system(f"docker push sehooh5/{docker_name}:latest")
    os.chdir("/home/keti0/keti/Project1-1/REST_API/manager")

    return render_template('apply_doc.html')

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
