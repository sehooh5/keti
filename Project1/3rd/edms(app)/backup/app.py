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

@app.route('/')
def index():
    return "Index"

@app.route('/drvl', methods=['GET'])
def drvl():
    arg = request.args.get('msg')


    print(arg)

    return arg

if __name__ == '__main__':
    app.run(host="0.0.0.0", threaded=True, port=5050)