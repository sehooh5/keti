#!/usr/bin/env python
from importlib import import_module
from flask import Flask, render_template, Response, request


app = Flask(__name__)


@app.route('/', methods=['GET'])
def index():
    """index"""
    return render_template('index.html')


if __name__ == '__main__':
    app.run(host='0.0.0.0', threaded=True, port=5040)
