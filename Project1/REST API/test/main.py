from flask import Flask, render_template, Response, request
from flask_socketio import SocketIO
from importlib import import_module
import os

app = Flask(__name__)
app.config['SECRET_KEY'] = 'keti'
socketio = SocketIO(app)


@app.route('/')
def sessions():
    return render_template('session.html')


def messageReceived(methods=['POST']):
    print('message was received!!!')


@socketio.on('my event')
def handle_my_custom_event(json, methods=['POST']):
    print('received my event: ' + str(json))
    # print(str(json['url']))
    if 'url' in str(json):
        url = str(json['url'])
        os.environ['URL'] = url
        print("os.environ['URL'] : " + os.environ['URL'])  # 여기까지 했음!!!
    socketio.emit('my response', json)


if __name__ == '__main__':
    socketio.run(app, host='0.0.0.0', port=5000, debug=True)
