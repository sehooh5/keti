from flask_socketio import SocketIO, emit, disconnect, send
from flask import Flask, render_template, session, request, Response
from importlib import import_module
import RPi.GPIO as GPIO
import sys
import time
from threading import Thread, Lock
import eventlet
eventlet.monkey_patch()


app = Flask(name)


async_mode = "eventlet"
socketio = SocketIO(app, async_mode=async_mode,
                    logger=True, engineio_logger=True)


def main_thread():


{'code stuff'}


@app.route('/')
@app.route('/index')
def index():
    return render_template('index.html', async_mode=socketio.async_mode)


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


Camera = import_module('camera_pi').Camera
thread = Thread(None, target=main_thread)
thread.start()


if name == 'main':
    socketio.run(app, host='127.0.0.1', port=5000, debug=False)
