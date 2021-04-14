#!/usr/bin/env python
from importlib import import_module
import os
from flask import Flask, render_template, Response, request

app = Flask(__name__)


@app.route('/')
def select():
    """Video streaming home page."""
    return render_template('manager.html')
#!/usr/bin/env python


@app.route('/writeDocker')
def write_docker():
    return render_template('write_doc.html')


@app.route('/saveDocker', methods=['GET', 'POST'])
def upload_file():
    if request.method == 'POST':
        docker_file = request.form['docker']
        folder_name = request.form['folder']
        file_name = request.form['fileName']
        # print(docker_file)

        # file 작성부분
        f = open(
            f'C:/Users/KETI/Desktop/keti/Project1-1/REST API/{folder_name}/{file_name}', 'w')
        f.write(docker_file)
        f.close()
    return render_template('apply_doc.html')


if __name__ == '__main__':
    app.run()
