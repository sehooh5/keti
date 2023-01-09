#!/usr/bin/env python
from importlib import import_module
import os
from flask import Flask, render_template, Response, request
import json

# 카메라 opencv 로 처음부터 지정
Camera = import_module('camera_opencv').Camera

app = Flask(__name__)


@app.route('/', methods=['POST'])
def viewer():
    """streaming"""
    json_data = request.get_json(silent=True)
    cam_url = json_data['cam_url']
    print(cam_url)

    if cam_url != 'stop':
        os.environ['OPENCV_CAMERA_SOURCE'] = cam_url
        os.environ['CAMERA_STOP'] = 'None'
        return render_template('cam.html', cam_no="CCTV Camera-1", worker_no="Worker 1")
    elif cam_url == 'stop':
        os.environ['CAMERA_STOP'] = 'stop'
        return render_template('cam.html', cam_no="Camera Loading...", worker_no="Worker 1")


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
    app.run(host='0.0.0.0', threaded=True, port=5555)
