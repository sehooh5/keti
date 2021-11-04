#!/usr/bin/env python
from flask import Flask, render_template, Response, request, jsonify
from flask_cors import CORS, cross_origin

app = Flask(__name__)
app.config['JSON_AS_ASCII'] = False 
CORS(app)


@app.route('/')
def index():

    return render_template('index.html')


if __name__ == '__main__':
    app.run(host='0.0.0.0', threaded=True, port=5000)
