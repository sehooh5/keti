import os
import json
import socket
import requests
from flask import Flask, render_template, Response, request, jsonify
from flask_cors import CORS, cross_origin
from threading import Thread

app = Flask(__name__)
app.config['JSON_AS_ASCII'] = False
CORS(app)

# print(socket.gethostname()) # DESKTOP-5OUO6UM
host_ip = socket.gethostbyname((socket.gethostname())) # 내부 IP : 192.168.0.20
ex_ip = requests.get("https://api.ipify.org").text # 외부 IP : 123.214.186.244

@app.route('/')
def index():
    return "Index"

@app.route('/act_device', methods=['POST'])
def act_device():
    json_data = request.get_json(silent=True)
    if json_data == None:
        res = {
            'code': '0020',
            'message': '데이터 Missing 오류'
        }
        return json.dumps(res, ensure_ascii=False)
    json_data = json_data['d_list']

    def act_cvlc(rtp_port, rtsp_port):
        os.system(
            f'cvlc -vvv rtp://:{rtp_port} --sout="#rtp{{sdp=rtsp://:{rtsp_port}/videoMain}}" --no-sout-all --sout-keep')

    for data in json_data:
        rtp_port = data['rtp_port']
        rtsp_port = str(int(rtp_port)+3550)
        print(f"rtp 포트번호 {rtp_port}와 rtsp 포트번호 {rtsp_port}로 실행 ")
        th = Thread(target=act_cvlc, args=(rtp_port, rtsp_port))
        th.start()

    return "200"

if __name__ == '__main__':
    app.run(host="0.0.0.0", threaded=True, port=5004)