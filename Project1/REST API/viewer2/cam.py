#!/usr/bin/env python
from importlib import import_module
import os
from flask import Flask, render_template, Response, request

# 카메라 opencv 로 처음부터 지정
Camera = import_module('camera_opencv').Camera

app = Flask(__name__)


@app.route('/', methods=['POST'])
def viewer():
    """streaming"""
    cam_no = request.form['cam_no']
    worker_no = request.form['worker_no']
    if cam_no == 'cam1':
        os.environ['OPENCV_CAMERA_SOURCE'] = 'rtsp://keti:keti1234@192.168.100.70:8810/videoMain'
        return render_template('cam1.html', cam_no=cam_no, worker_no=worker_no)
    elif cam_no == 'cam2':
        os.environ['OPENCV_CAMERA_SOURCE'] = 'rtsp://keti:keti1234@192.168.100.60:8805/videoMain'
        return render_template('cam2.html', cam_no=cam_no, worker_no=worker_no)


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
    app.run(host='0.0.0.0', threaded=True, port=5001)
