from flask import Blueprint, request
import requests
import json

edge_bp = Blueprint('edge', __name__)

@edge_bp.route('/save_edgeData', methods=['POST'])
def save_edgeData():
    nip = request.remote_addr
    res = requests.get(f"http://192.168.0.9:5230/get_nid_by_ip?nip={nip}")
    if res.status_code == 200:
        json_data = res.json()
        nid = json_data.get('nid')

    # Continue processing...
    return "edge data saved"
