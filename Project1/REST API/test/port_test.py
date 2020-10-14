#!/usr/bin/env python
from importlib import import_module
import os
from flask import Flask, render_template, Response, request

app = Flask(__name__)


@app.route('/')
def select():
    return render_template('client.html')


if __name__ == '__main__':
    app.run(host='0.0.0.0', threaded=True, port=5000)
