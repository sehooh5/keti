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
    cam_no = request.form['cam_no']
    worker_no = request.form['worker_no']
    if cam_no == 'Camera1':
        os.environ['OPENCV_CAMERA_SOURCE'] = 'rtsp://keti:keti1234@192.168.100.70:8810/videoMain'
        os.environ['CAMERA_STOP'] = 'None'
        return render_template('cam1.html', cam_no="CCTV Camera-1", worker_no=worker_no)
    elif cam_no == 'Camera2':
        os.environ['OPENCV_CAMERA_SOURCE'] = 'rtsp://keti:keti1234@192.168.100.60:8805/videoMain'
        os.environ['CAMERA_STOP'] = 'None'
        return render_template('cam1.html', cam_no="CCTV Camera-2", worker_no=worker_no)
    elif cam_no == 'stop':
        os.environ['CAMERA_STOP'] = 'stop'
        return render_template('cam1.html', cam_no="Camera Loading...", worker_no=worker_no)


# @app.route('/test', methods=['POST'])
# def test():
#     data = json.loads(request.get_data(), encoding='utf-8')
#     if len(data) == 0:
#         return "No data!!"

#     print(data['cam_no'], data['worker_no'])

#     cam_no = data['cam_no']
#     worker_no = data['worker_no']

#     if cam_no == 'Camera1':
#         os.environ['OPENCV_CAMERA_SOURCE'] = 'rtsp://keti:keti1234@192.168.100.70:8810/videoMain'
#         os.environ['CAMERA_STOP'] = 'None'
#         return render_template('cam1.html', cam_no="CCTV Camera-1", worker_no=worker_no)
#     elif cam_no == 'Camera2':
#         os.environ['OPENCV_CAMERA_SOURCE'] = 'rtsp://keti:keti1234@192.168.100.60:8805/videoMain'
#         os.environ['CAMERA_STOP'] = 'None'
#         return render_template('cam1.html', cam_no="CCTV Camera-2", worker_no=worker_no)
#     elif cam_no == 'stop':
#         os.environ['CAMERA_STOP'] = 'stop'
#         return render_template('cam1.html', cam_no="Camera Loading...", worker_no=worker_no)


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
