from flask import Flask, render_template, Response, request, jsonify
from flask_cors import CORS, cross_origin
from datetime import datetime

app = Flask(__name__)
# app.config['JSON_AS_ASCII'] = False
# CORS(app)
port = "5000"

@app.route('/')
def index():

    time_data =datetime.now()

    return render_template('index.html', time_data = time_data)

if __name__ == '__main__':
    app.run(host='0.0.0.0', threaded=True, port=port)