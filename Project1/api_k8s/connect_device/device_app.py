#!/usr/bin/env python
from importlib import import_module
import os
from flask import Flask, render_template, Response, request
from flask_socketio import SocketIO, send

Camera = import_module('camera_opencv').Camera


app = Flask(__name__)
app.config['SECRET_KEY'] = 'SEHO_Flask'
socketio = SocketIO(app)


@socketio.on('nodeport')
def handle_nodeport(data):
    print('received nodeport: ' + data)


@socketio.on('device_url')
def handle_device_url(data):
    os.environ['OPENCV_CAMERA_SOURCE'] = data
    print("카메라 소스 : ", os.environ['OPENCV_CAMERA_SOURCE'])


@app.route('/')
def select():
    """Video streaming home page."""
    return render_template('select.html')


@app.route('/cam', methods=['GET'])
def camera():
    """Camera1 streaming"""
    # url 의 파라미터 값을 가져오는 방법
    no = request.args.get('no')

    # device_url = os.environ['OPENCV_CAMERA_SOURCE']
    print(os.environ['OPENCV_CAMERA_SOURCE'])
    # if no == '1':
    #     os.environ['OPENCV_CAMERA_SOURCE'] = device_url
    # elif no == '2':
    #     os.environ['OPENCV_CAMERA_SOURCE'] = 'rtsp://keti:keti1234@192.168.100.60:8805/videoMain'

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
    socketio.run(app, host="0.0.0.0", port=5000, debug=True)
