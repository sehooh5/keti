#!/usr/bin/env python
import os
from importlib import import_module

import requests
from flask import Flask, Response, jsonify, render_template, request
import json

app = Flask(__name__)


@app.route('/')
def select():
    """Video streaming home page."""
    return render_template('manager_app.html')


@app.route('/2')
def connect():
    """Video streaming home page."""
    return render_template('manager_app2.html')


@app.route('/index')
def index():
    """INDEX"""
    return render_template('index.html')


@app.route('/test', methods=['POST'])
def connect_device_test():

    cam_no = request.form['cam_no']
    worker_no = request.form['worker_no']
    nodeport = request.form['nodeport']

    print(cam_no, worker_no, nodeport)

    data = {
        "cam_no": cam_no,
    }

    requests.post(f"http://localhost:{nodeport}/test", data=json.dumps(data))

    res = jsonify(
        code="0000",
        message="처리 성공"
    )
    return res


if __name__ == '__main__':
    app.run(host='0.0.0.0', threaded=True, port=5051)
