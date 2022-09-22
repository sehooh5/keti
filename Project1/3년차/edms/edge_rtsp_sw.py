import os
import json
import socket
import requests
from flask import Flask, render_template, Response, request, jsonify
from flask_cors import CORS, cross_origin

app = Flask(__name__)
app.config['JSON_AS_ASCII'] = False
CORS(app)

# print(socket.gethostname()) # DESKTOP-5OUO6UM
host_ip = socket.gethostbyname((socket.gethostname())) # 내부 IP : 192.168.0.20
ex_ip = requests.get("https://api.ipify.org").text # 외부 IP : 123.214.186.244
print(ex_ip)

@app.route('/')
def index():
    return "Index"

@app.route('/device_ids', methods=['POST'])
def device_ids():
    json_data = request.get_json(silent=True)
    print(json_data)

    return "200"

if __name__ == '__main__':
    app.run(host="0.0.0.0", threaded=True, port=5004)