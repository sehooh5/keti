#!/usr/bin/env python
## app.py 기반 master 에서 실행되는 서버
from importlib import import_module
from typing import List
from flask import Flask, render_template, Response, request, jsonify
from flask_cors import CORS, cross_origin
import json
import requests
import os
import response
import string

app = Flask(__name__)
app.config['JSON_AS_ASCII'] = False  # jsonify 한글깨짐 해결
CORS(app)

# 랜덤한 문자열 생성기
_LENGTH = 4
string_pool = string.ascii_letters + string.digits

API_URL = "http://192.168.0.9:5230"

port = "6432"

@ app.route('/request_upload_edgeAi', methods=['POST'])
def request_upload_edgeAi():
    try:
        


        return response.message('0000')

    except json.JSONDecodeError:
        return response.message('0010')

    except KeyError as e:
        return response.message('0015')

    except ValueError as e:
        return response.message('9999')

@ app.route('/request_remove_edgeAi', methods=['POST'])
def request_remove_edgeAi():
    try:
        data = request.get_json(silent=True)
        if data is None:
            raise ValueError("No JSON data received")

        json_data = json.loads(data)

        nid = json_data.get('nid')
        created_at = json_data.get('cpu')
        res_class = json_data.get('memory')
        res_confidence = json_data.get('res_confidence')

        if not all([nid, created_at, res_class, res_confidence]):
            raise KeyError("Missing required fields in the request")

        print(f"Node ID: {nid} // Created time: {created_at} // Weather Class: {res_class} // Confidence: {res_confidence}")

        return response.message('0000')

    except json.JSONDecodeError:
        return response.message('0010')

    except KeyError as e:
        return response.message('0015')

    except ValueError as e:
        return response.message('9999')

@ app.route('/request_deploy_aiToDevice ', methods=['POST'])
def request_deploy_aiToDevice ():
    try:
        data = request.get_json(silent=True)
        if data is None:
            raise ValueError("No JSON data received")

        json_data = json.loads(data)

        nid = json_data.get('nid')
        created_at = json_data.get('cpu')
        res_class = json_data.get('memory')
        res_confidence = json_data.get('res_confidence')

        if not all([nid, created_at, res_class, res_confidence]):
            raise KeyError("Missing required fields in the request")

        print(f"Node ID: {nid} // Created time: {created_at} // Weather Class: {res_class} // Confidence: {res_confidence}")

        return response.message('0000')

    except json.JSONDecodeError:
        return response.message('0010')

    except KeyError as e:
        return response.message('0015')

    except ValueError as e:
        return response.message('9999')

@ app.route('/request_undeploy_aiFromDevice', methods=['POST'])
def request_undeploy_aiFromDevice():
    try:
        data = request.get_json(silent=True)
        if data is None:
            raise ValueError("No JSON data received")

        json_data = json.loads(data)

        nid = json_data.get('nid')
        created_at = json_data.get('cpu')
        res_class = json_data.get('memory')
        res_confidence = json_data.get('res_confidence')

        if not all([nid, created_at, res_class, res_confidence]):
            raise KeyError("Missing required fields in the request")

        print(f"Node ID: {nid} // Created time: {created_at} // Weather Class: {res_class} // Confidence: {res_confidence}")

        return response.message('0000')

    except json.JSONDecodeError:
        return response.message('0010')

    except KeyError as e:
        return response.message('0015')

    except ValueError as e:
        return response.message('9999')

@ app.route('/get_selectedEdgeAiInfo', methods=['POST'])
def get_selectedEdgeAiInfo():
    try:
        data = request.get_json(silent=True)
        if data is None:
            raise ValueError("No JSON data received")

        json_data = json.loads(data)

        nid = json_data.get('nid')
        created_at = json_data.get('cpu')
        res_class = json_data.get('memory')
        res_confidence = json_data.get('res_confidence')

        if not all([nid, created_at, res_class, res_confidence]):
            raise KeyError("Missing required fields in the request")

        print(f"Node ID: {nid} // Created time: {created_at} // Weather Class: {res_class} // Confidence: {res_confidence}")

        return response.message('0000')

    except json.JSONDecodeError:
        return response.message('0010')

    except KeyError as e:
        return response.message('0015')

    except ValueError as e:
        return response.message('9999')

if __name__ == '__main__':
    app.run(host='0.0.0.0', threaded=True, port=port)
