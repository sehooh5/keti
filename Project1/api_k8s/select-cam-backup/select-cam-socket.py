import os
from importlib import import_module
from flask import Flask, render_template, Response, request, jsonify
import json
from flask_socketio import SocketIO


Camera = import_module('camera_opencv').Camera


app = Flask(__name__)
app.config['SECRET_KEY'] = 'SEHO_SOCKETIO'
socketio = SocketIO(app)

del_url = "echo keti | sudo -S sed -i '/OPENCV_CAMERA_SOURCE/d' ~/.bashrc"
del_stop = "echo keti | sudo -S sed -i '/CAMERA_STOP/d' ~/.bashrc"
refresh = "/bin/bash -c 'source ~/.bashrc'"


@app.route('/streaming', methods=['GET'])
def streaming():
    """streaming"""

    if "OPENCV_CAMERA_SOURCE" in os.environ:
        cam_url = os.environ['OPENCV_CAMERA_SOURCE']
        print("Camera Name : ", os.environ['CAMERA_NAME'])
        print("환경변수 : ", cam_url, flush=True)

        cam_name = os.environ['CAMERA_NAME']

        if os.environ['CAMERA_STOP'] == "None":
            return render_template('cam.html', cam_name=cam_name, worker_no=os.uname().nodename)
        elif os.environ['CAMERA_STOP'] == "stop":
            return render_template('cam_stop.html', worker_no=os.uname().nodename)
    else:
        return render_template('cam_stop.html')


@app.route('/connect', methods=['POST'])
def connect():
    """getting cam information"""
    json_data = json.loads(request.get_data(), encoding='utf-8')

    cam_url = json_data['url']
    cam_name = json_data['name']

    os.environ['CAMERA_NAME'] = cam_name

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
    handle_my_custom_event('connect')
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


@app.route('/ajax_data', methods=['GET'])
def ajax_data():
    data = os.environ['CAMERA_STOP']

    res = jsonify(
        code="0000",
        message="처리 성공",
        data=data
    )

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


@app.route('/')
def sessions():
    return render_template('session.html')


@socketio.on('connect')
def test_connect():
    print("socket connected")


@socketio.on('my event')
def handle_my_custom_event(data):
    socketio.emit('my response', data, broadcast=True)


if __name__ == '__main__':
    socketio.run(app, host='0.0.0.0', port=5050, debug=True)
