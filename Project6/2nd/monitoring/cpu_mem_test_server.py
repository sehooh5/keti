from flask import Flask, render_template, Response, request, jsonify
from flask_cors import CORS, cross_origin
import json
import response

app = Flask(__name__)
app.config['JSON_AS_ASCII'] = False  # jsonify 한글깨짐 해결
CORS(app)

@app.route('/usage', methods=['POST'])
def usage():
    data = request.get_json(silent=True)
    json_data = json.loads(data)

    username = json_data['username']
    cpu_usage = json_data['cpu']
    memory_usage = json_data['memory']

    print(f"User Name : {uname}, CPU Usage : {cpu_usage}%, Memory Usage : {memory_usage}%")

    return "index"


app.run(host="192.168.0.14",port="6432")