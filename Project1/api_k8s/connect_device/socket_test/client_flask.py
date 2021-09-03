import socketio
from flask import Flask, render_template, Response, request, jsonify

app = Flask(__name__)
app.config['JSON_AS_ASCII'] = False


@app.route("/")
def index():
    return render_template('index.html')


@app.route("/connect_device", methods=['POST'])
def connect_device():

    sio = socketio.Client()

    sio.connect('http://localhost:5000')

    # nodeport = "30000"
    # device_url = "rtsp://keti:keti1234@192.168.100.60:8805/videoMain"
    nodeport = request.form['nodeport']
    device_url = request.form['device_url']
    print(nodeport, device_url)
    sio.emit('nodeport', nodeport)
    sio.emit('device_url', device_url)

    sio.sleep(5)
    sio.disconnect()

    res = jsonify(
        code="0000",
        message="처리 성공"
    )
    return render_template('index.html')


@app.route("/disconnect_device", methods=['POST'])
def disconnect_device():

    sio = socketio.Client()

    sio.connect('http://localhost:5000')

    # nodeport = "30000"
    # device_url = "rtsp://keti:keti1234@192.168.100.60:8805/videoMain"
    nodeport = request.form['nodeport']
    print(nodeport)
    sio.emit('nodeport', nodeport)
    sio.emit('device_url', "STOP")

    sio.sleep(5)
    sio.disconnect()

    res = jsonify(
        code="0000",
        message="처리 성공"
    )
    return render_template('index.html')


if __name__ == '__main__':
    app.run(host="0.0.0.0", port=5050, debug=True)
