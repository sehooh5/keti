import socketio
from flask import Flask, render_template, Response, request, jsonify

app = Flask(__name__)
app.config['JSON_AS_ASCII'] = False


@app.route("/")
def index():
    return render_template('index.html')


@app.route("/connect_device", methods=['POST'])
def connect_device():

    data = request.get_json(silent=True)
    print(data)

    eid = data['eid']
    did = data['did']
    print(eid, did)

    res = jsonify(
        code="0000",
        message="처리 성공"
    )
    return res


@app.route("/disconnect_device", methods=['POST'])
def disconnect_device():

    data = request.get_json(silent=True)
    print(data)

    eid = data['eid']
    did = data['did']
    print(eid, did)

    res = jsonify(
        code="0000",
        message="처리 성공"
    )
    return res

    return render_template('index.html')


if __name__ == '__main__':
    app.run(host="0.0.0.0", port=5009, debug=True)
