import os
from importlib import import_module
from flask import Flask, render_template, Response, request
import json


Camera = import_module('camera_opencv').Camera


app = Flask(__name__)

del_url = "echo keti | sudo -S sed -i '/OPENCV_CAMERA_SOURCE/d' ~/.bashrc"
del_stop = "echo keti | sudo -S sed -i '/CAMERA_STOP/d' ~/.bashrc"
refresh = "/bin/bash -c 'source ~/.bashrc'"


@app.route('/streaming', methods=['GET'])
def streaming():
    """streaming"""

    if "OPENCV_CAMERA_SOURCE" in os.environ:
        cam_url = os.environ['OPENCV_CAMERA_SOURCE']
        print("환경변수 : ", cam_url, flush=True)

        if cam_url.find("8805") != -1:
            cam_no = "CCTV Camera 1"
        elif cam_url.find("8810") != -1:
            cam_no = "CCTV Camera 2"
        else:
            cam_no = "CCTV Camera 3"

        if os.environ['CAMERA_STOP'] == "None":
            return render_template('cam.html', cam_no=cam_no, worker_no=os.uname().nodename)
        elif os.environ['CAMERA_STOP'] == "stop":
            return render_template('cam_stop.html')
    else:
        return render_template('cam_stop.html')


@app.route('/connect', methods=['POST'])
def connect():
    """getting cam information"""
    json_data = json.loads(request.get_data(), encoding='utf-8')

    cam_url = json_data['url']

    os.system(del_url)
    os.system(del_stop)
    os.system(
        f"echo keti | sudo -S echo 'export OPENCV_CAMERA_SOURCE={cam_url}' >> ~/.bashrc")
    os.system("echo keti | sudo -S echo 'export CAMERA_STOP=None' >> ~/.bashrc")
    os.system(refresh)

    os.environ['OPENCV_CAMERA_SOURCE'] = cam_url
    os.environ['CAMERA_STOP'] = "None"
    print("카메라 소스 : ", os.environ['OPENCV_CAMERA_SOURCE'], flush=True)
    print("카메라 스탑 상태 : ", os.environ['CAMERA_STOP'], flush=True)
    res = f"Camera connect with URL : {cam_url}"
    return res


@app.route('/disconnect', methods=['POST'])
def disconnect():
    json_data = json.loads(request.get_data(), encoding='utf-8')

    cam_url = json_data['url']
    os.system(del_url)
    os.system(del_stop)
    os.system("echo keti | sudo -S echo 'export CAMERA_STOP=stop' >> ~/.bashrc")
    os.system(refresh)
    os.environ['OPENCV_CAMERA_SOURCE'] = "None"
    os.environ['CAMERA_STOP'] = "stop"
    print("카메라 소스 : ", os.environ['OPENCV_CAMERA_SOURCE'], flush=True)
    print("카메라 스탑 상태 : ", os.environ['CAMERA_STOP'], flush=True)
    res = f"Camera disconnect with URL : {cam_url}"
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
    app.run(host='0.0.0.0', threaded=True, port=5050)
