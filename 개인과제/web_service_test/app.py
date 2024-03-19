from flask import Flask, render_template, Response, request, jsonify
from flask_cors import CORS, cross_origin
from datetime import datetime

app = Flask(__name__)
# app.config['JSON_AS_ASCII'] = False
# CORS(app)

@app.route('/')
def index():
    print(datetime.now())
    return render_template('index.html')


 