#!/usr/bin/env python
from importlib import import_module
from flask import Flask, render_template, Response, request
import os
import subprocess

app = Flask(__name__)


@app.route('/')
def select():
    """Video streaming home page."""
    return render_template('manager.html')
#!/usr/bin/env python


@app.route('/writeFile')
def write_file():
    return render_template('write_doc.html')


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
    # 테스트 해보는중
    # 1. os 모듈사용
    #os.system("mkdir my_working")

    if request.method == 'POST':
        file = request.form['file']
        fileName = request.form['fileName']

        os.system("echo %s" % fileName)

    # 2. subprocess 모듈사용
    # subprocess.call('echo hi, Worker', shell=True)

    return render_template('function_test.html')


@app.route('/build', methods=['GET', 'POST'])
def build():
    print("@@@ docker build start @@@")
    if request.method == 'POST':
        folder_name = request.form['folder']
        file_name = request.form['fileName']
        path = os.getcwd().replace("manager", f'{folder_name}/')
        print(f"@@@ docker path = {path} @@@")
        print(f"docker build -f {file_name} -t sehooh5/build_test:latest ")
        os.system(
            f"docker build -f {file_name} -t sehooh5/build_test:latest {path}")
        print("@@@ building success!! @@@")
    return render_template('function_test.html')


@app.route('/push', methods=['GET', 'POST'])
def push():

    if request.method == 'POST':
        file = request.form['file']
        fileName = request.form['fileName']
        os.system("ls")

    return render_template('function_test.html')


if __name__ == '__main__':
    app.run()
