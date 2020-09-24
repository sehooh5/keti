#!/usr/bin/env python
from importlib import import_module
import os
from flask import Flask, render_template, Response, request

# import camera driver
if os.environ.get('CAMERA'):
    Camera = import_module('camera_' + os.environ['CAMERA']).Camera
else:
    from camera import Camera

# Raspberry Pi camera module (requires picamera package)
# from camera_pi import Camera

app = Flask(__name__)


@app.route('/')
def select():
    """Video streaming home page."""
    return render_template('select.html')


@app.route('/cam', methods=['GET'])
def camera():
    """Camera1 streaming"""
    # url 의 파라미터 값을 가져오는 방법
    no = request.args.get('no')
    print('number = '+request.args.get('no'))
    if no == '1':
        os.environ['OPENCV_CAMERA_SOURCE'] = 'rtsp://keti:keti1234@192.168.100.70:8810/videoMain'
        print(os.environ['OPENCV_CAMERA_SOURCE'])
    elif no == '2':
        os.environ['OPENCV_CAMERA_SOURCE'] = 'rtsp://keti:keti1234@192.168.100.60:8805/videoMain'

    return render_template('camera.html')


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
    app.run(host='0.0.0.0', threaded=True)
