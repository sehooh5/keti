#!/usr/bin/env python
from importlib import import_module
import os
from flask import Flask, render_template, Response, request

# 1. import camera driver
# if os.environ.get('CAMERA'):
#     Camera = import_module('camera_' + os.environ['CAMERA']).Camera
# else:
#     from camera import Camera

# 2. 카메라 opencv 로 처음부터 지정
Camera = import_module('camera_opencv').Camera


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
    # print('number = '+request.args.get('no'))
    if no == '1':
        os.environ['OPENCV_CAMERA_SOURCE'] = 'rtsp://root:keti@192.168.0.94/onvif-media/media.amp'
    elif no == '2':
        os.environ['OPENCV_CAMERA_SOURCE'] = 'rtsp://root:keti@192.168.0.93/onvif-media/media.amp'

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
    app.run(host='0.0.0.0', threaded=True, port=5058)
