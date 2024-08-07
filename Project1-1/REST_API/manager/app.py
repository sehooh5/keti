#!/usr/bin/env python
from importlib import import_module
from flask import Flask, render_template, Response, request, jsonify
import os
import subprocess

app = Flask(__name__)
app.config['JSON_AS_ASCII'] = False


@app.route('/')
def select():
    return render_template('manager.html')


@app.route('/writeFile')
def write_file():
    s = """NAME STATUS ROLES AGE VERSION
keti0-master Ready master 336d v1.18.8
keti1-worker1 Ready 336d v1.18.6
keti2-worker2 Ready 336d v1.18.6"""

    s_split = s.split('\n')
    len_s = len(s_split)

    n_list = s_split[1:len_s]
    names = []
    for x in n_list:
        nx = {"name" : x.split(' ')[0]}
        names.append(nx)

    res = jsonify(
        code = "0000",
        message = "처리 성공",
        nlist = names
    )
    print("담기긴한다 ㅎㅎ")
    return res


@app.route('/saveFile', methods=['GET', 'POST'])
def upload_file():
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


if __name__ == '__main__':
    app.run()
