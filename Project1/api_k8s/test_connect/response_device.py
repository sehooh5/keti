#!/usr/bin/env python
from importlib import import_module
import os
from flask import Flask, render_template, Response, request
import json
import subprocess

# 카메라 opencv 로 처음부터 지정
Camera = import_module('camera_opencv').Camera

app = Flask(__name__)

del_url = "echo keti | sudo sed -i '/OPENCV_CAMERA_SOURCE/d' ~/.bashrc"
del_stop = "echo keti | sudo sed -i '/CAMERA_STOP/d' ~/.bashrc"
refresh = "source ~/.bashrc"


@app.route('/streaming', methods=['GET'])
def streaming():
    """streaming"""
    return render_template('cam.html', cam_no="CCTV Camera", worker_no="keti1-worker1")


@app.route('/connect', methods=['POST'])
def connect():
    """getting cam information"""
    json_data = json.loads(request.get_data(), encoding='utf-8')

    print("카메라 URL : ", json_data['url'])

    cam_url = json_data['url']

    os.system(del_url)
    os.system(del_stop)
    os.system(
        "echo keti | sudo echo 'export OPENCV_CAMERA_SOURCE={cam_url}' >> ~/.bashrc")
    os.system("echo keti | sudo echo 'export CAMERA_STOP=None' >> ~/.bashrc")
    os.system(refresh)
    res = f"Camera connect with URL : {cam_url}"
    return res


@app.route('/disconnect', methods=['POST'])
def disconnect():
    json_data = json.loads(request.get_data(), encoding='utf-8')

    print("카메라 URL : ", json_data['url'])

    cam_url = json_data['url']
    os.system(del_url)
    os.system(del_stop)
    os.system("echo keti | sudo echo 'export CAMERA_STOP=stop' >> ~/.bashrc")
    os.system(refresh)
    res = f"Camera connect with URL : {cam_url}"
    return res


def gen(camera):
    """Video streaming generator function."""
    while True:
        frame = camera.get_frame()
        yield (b'--frame\r\n'
               b'Content-Type: image/jpeg\r\n\r\n' + frame + b'\r\n')


@app.route('/video_feed')
def video_feed():
    """Video streaming route. Put this in the src attribute of an img tag."""
    return Response(gen(Camera()),
                    mimetype='multipart/x-mixed-replace; boundary=frame')


if __name__ == '__main__':
    app.run(host='0.0.0.0', threaded=True, port=5061)
