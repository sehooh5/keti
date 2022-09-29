import paramiko
import os
import json
import socket
import requests
from flask import Flask, render_template, Response, request, jsonify
from flask_cors import CORS, cross_origin
from threading import Thread

app = Flask(__name__)
# 다른 서버에 명령 보낼때 사용
cli = paramiko.SSHClient()
cli.set_missing_host_key_policy(paramiko.AutoAddPolicy)

@app.route('/')
def index():
    return "Index"

@app.route('/param', methods=['GET'])
def param():
    cli.connect('192.168.0.28', port=22, username="keti2", password="keti")
    stdin, stdout, stderr = cli.exec_command("hostname", get_pty=True)
    stdin.write('keti\n')
    stdin.flush()
    lines = stdout.readlines()
    print(''.join(lines))

    cli.close()

    return "200"

if __name__ == '__main__':
    app.run(host="0.0.0.0", threaded=True, port=5000)

