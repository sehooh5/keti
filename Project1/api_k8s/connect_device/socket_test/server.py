from flask import Flask, render_template
from flask_socketio import SocketIO, send

app = Flask(__name__)
app.config['SECRET_KEY'] = 'SEHO_Flask'
socketio = SocketIO(app)


@app.route("/")
def main():
    return render_template("index.html")


@socketio.on('nodeport')
def handle_message(data):
    print('received nodeport: ' + data)


@socketio.on('device_url')
def handle_message(data):
    print('received device url: ' + data)


if __name__ == '__main__':
    socketio.run(app, host="0.0.0.0", port=5000)
