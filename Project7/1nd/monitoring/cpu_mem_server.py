from flask import Flask, render_template, Response, request, jsonify
from flask_cors import CORS, cross_origin
import json
import response
import time




app = Flask(__name__)
app.config['JSON_AS_ASCII'] = False  # jsonify 한글깨짐 해결
CORS(app)

latest_data = None
last_update = None
TIMEOUT_THRESHOLD = 5

@app.route('/usage', methods=['POST'])
def usage():
    global latest_data, last_update

    data = request.get_json(silent=True)

    if data:
        latest_data = data
        last_update = time.time()

        json_data = json.loads(data)

        username = json_data['username']
        cpu_usage = json_data['cpu']
        memory_usage = json_data['memory']
        time_now = last_update

        print(f"User Name : {username}, CPU Usage : {cpu_usage}%, Memory Usage : {memory_usage}%")

        return jsonify({"result": "success"})
    else:
        return jsonify({"result": "error", "message": "잘못된 데이터"}), 400


@app.route('/usage', methods=['GET'])
def get_usage():
    if latest_data is None or last_update is None or (time.time() - last_update > TIMEOUT_THRESHOLD):
        return jsonify({"message": "데이터 없음"}), 404
    else:
        return jsonify(latest_data)

app.run(host="192.168.0.14",port="6432")