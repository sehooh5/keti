#!/usr/bin/env python
# 1
# from base_camera import BaseCamera
import cv2
# 2
import time
import threading
import os
try:
    from greenlet import getcurrent as get_ident
except ImportError:
    try:
        from thread import get_ident
    except ImportError:
        from _thread import get_ident
###
from importlib import import_module
import os
from flask import Flask, render_template, Response, request
import json

# 카메라 opencv 로 처음부터 지정
# Camera = import_module('camera_opencv').Camera

# 한개로 합치기 연습
# base_camera.py


class CameraEvent(object):
    """An Event-like class that signals all active clients when a new frame is
    available.
    """

    def __init__(self):
        self.events = {}

    def wait(self):
        """Invoked from each client's thread to wait for the next frame."""
        ident = get_ident()
        if ident not in self.events:
            self.events[ident] = [threading.Event(), time.time()]
        return self.events[ident][0].wait()

    def set(self):
        """Invoked by the camera thread when a new frame is available."""
        now = time.time()
        remove = None
        for ident, event in self.events.items():
            if not event[0].isSet():
                event[0].set()
                event[1] = now
            else:
                if now - event[1] > 5:
                    remove = ident
        if remove:
            del self.events[remove]

    def clear(self):
        """Invoked from each client's thread after a frame was processed."""
        self.events[get_ident()][0].clear()


class BaseCamera(object):
    thread = None
    frame = None
    last_access = 0
    event = CameraEvent()

    def __init__(self):
        """Start the background camera thread if it isn't running yet."""
        if BaseCamera.thread is None:
            BaseCamera.last_access = time.time()
            BaseCamera.thread = threading.Thread(target=self._thread)
            BaseCamera.thread.start()

            while self.get_frame() is None:
                time.sleep(0)

    def get_frame(self):
        """Return the current camera frame."""
        BaseCamera.last_access = time.time()
        BaseCamera.event.wait()
        BaseCamera.event.clear()

        return BaseCamera.frame

    @staticmethod
    def frames():
        """"Generator that returns frames from the camera."""
        raise RuntimeError('Must be implemented by subclasses.')

    @classmethod
    def _thread(cls):
        """Camera background thread."""
        print('Starting camera thread.')
        frames_iterator = cls.frames()
        for frame in frames_iterator:
            BaseCamera.frame = frame
            BaseCamera.event.set()
            time.sleep(0)
            if time.time() - BaseCamera.last_access > 10:
                frames_iterator.close()
                print('Stopping camera thread due to inactivity.')
                break
            if os.environ['CAMERA_STOP'] == 'stop':
                frames_iterator.close()
                print('Stopping camera thread due to STOP!.')
                break
        BaseCamera.thread = None
# camera_opencv


class Camera(BaseCamera):
    video_source = 0
    print("0")

    def __init__(self):
        if os.environ.get('OPENCV_CAMERA_SOURCE'):
            Camera.set_video_source(os.environ['OPENCV_CAMERA_SOURCE'])
        super(Camera, self).__init__()

    @staticmethod
    def set_video_source(source):
        print("비디오 소스 : ", source)
        Camera.video_source = source

    @staticmethod
    def frames():
        camera = cv2.VideoCapture(Camera.video_source)
        if not camera.isOpened():
            raise RuntimeError('Could not start camera.')
        else:
            print("Video Streaming On !")
        while True:
            _, img = camera.read()

            yield cv2.imencode('.jpg', img)[1].tobytes()


app = Flask(__name__)

del_url = "echo keti | sudo -S sed -i '/OPENCV_CAMERA_SOURCE/d' ~/.bashrc"
del_stop = "echo keti | sudo -S sed -i '/CAMERA_STOP/d' ~/.bashrc"
refresh = "/bin/bash -c 'source ~/.bashrc'"


@app.route('/streaming', methods=['GET'])
def streaming():
    """streaming"""
    cam_url = os.environ['OPENCV_CAMERA_SOURCE']
    print("환경변수 : ", cam_url, flush=True)

    if cam_url.find("8810") == -1:
        cam_no = "CCTV Camera 2"
    else:
        cam_no = "CCTV Camera 1"
    if os.environ['CAMERA_STOP'] == "None":
        return render_template('cam.html', cam_no=cam_no, worker_no=os.uname().nodename)
    elif os.environ['CAMERA_STOP'] == "stop":
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
    print("카메라 소스 : ", os.environ['OPENCV_CAMERA_SOURCE'])
    print("카메라 스탑 상태 : ", os.environ['CAMERA_STOP'])
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
    print("카메라 소스 : ", os.environ['OPENCV_CAMERA_SOURCE'])
    print("카메라 스탑 상태 : ", os.environ['CAMERA_STOP'])
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
