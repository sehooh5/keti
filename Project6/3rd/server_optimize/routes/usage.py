from flask import Blueprint, request

usage_bp = Blueprint('usage', __name__)

@usage_bp.route('/', methods=['POST'])
def usage():
    data = request.get_json(silent=True)
    json_data = data
    username = json_data['username']
    cpu_usage = json_data['cpu']
    memory_usage = json_data['memory']
    ai_class = json_data['ai_class']

    return "usage data received"
