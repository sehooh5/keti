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
    ip = '192.168.0.28'
    hname = "keti2"
    pwd = "keti"
    cli.connect(ip, port=22, username=hname, password=pwd)
    stdin, stdout, stderr = cli.exec_command("ls", get_pty=True)
    stdin.write('keti\n')
    stdin.flush()
    lines = stdout.readlines()
    print("print : ", ''.join(lines))

    cli.close()

    return "200"

@app.route('/worker', methods=['GET'])
def worker():
    ip = '192.168.0.25'
    hname = "keti1"
    pwd = "keti"
    cli.connect(ip, port=22, username=hname, password=pwd)
    stdin, stdout, stderr = cli.exec_command("ls", get_pty=True)
    stdin.write('keti\n')
    stdin.flush()
    lines = stdout.readlines()
    print("print : ",''.join(lines))

    cli.close()

    return "200"

if __name__ == '__main__':
    app.run(host="0.0.0.0", threaded=True, port=5000)

