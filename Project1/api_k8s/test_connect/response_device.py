#!/usr/bin/env python
from importlib import import_module
import os
from flask import Flask, render_template, Response, request
import json
import subprocess

# 카메라 opencv 로 처음부터 지정
Camera = import_module('camera_opencv').Camera

app = Flask(__name__)


@app.route('/', methods=['POST'])
def viewer():
    """streaming"""

    del_url = "echo keti | sudo sed -i '/OPENCV_CAMERA_SOURCE/d' ~/.bashrc"
    del_stop = "echo keti | sudo sed -i '/CAMERA_STOP/d' ~/.bashrc"
    refresh = "source ~/.bashrc"

    json_data = json.loads(request.get_data(), encoding='utf-8')
    print("카메라 넘버 : ", json_data['cam_no'])

    cam_no = json_data['cam_no']
    if cam_no == '1':
        os.system(del_url)
        os.system(del_stop)
        os.system(
            "sudo echo 'export OPENCV_CAMERA_SOURCE=rtsp://keti:keti1234@192.168.100.70:8810/videoMain' >> ~/.bashrc")
        os.system("sudo echo 'export CAMERA_STOP=None' >> ~/.bashrc")
        os.system(refresh)
        res = "ㅎㅇ"
        return res
    elif cam_no == '2':
        os.system(del_url)
        os.system(del_stop)
        os.system(
            "sudo echo 'export OPENCV_CAMERA_SOURCE=rtsp://keti:keti1234@192.168.100.60:8805/videoMain' >> ~/.bashrc")
        os.system("sudo echo 'export CAMERA_STOP=None' >> ~/.bashrc")
        os.system(refresh)
        res = "ㅎㅇ2"
        return res
    elif cam_no == 'stop':
        os.environ['CAMERA_STOP'] = 'stop'
        return render_template('cam1.html', cam_no="Camera Loading...", worker_no=worker_no)


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
