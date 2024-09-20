from flask import Blueprint, request, jsonify
import response

weather_bp = Blueprint('weather', __name__)

@weather_bp.route('/optimize_by_weather', methods=['POST'])
def optimize_by_weather():
    try:
        data = request.get_json(silent=True)
        if not data:
            raise ValueError("No JSON data received")

        json_data = data
        nid = json_data.get('nid')
        cpu = json_data.get('cpu')
        memory = json_data.get('memory')
        res_confidence = json_data.get('res_confidence')

        print(f"Node ID: {nid}, CPU: {cpu}, Memory: {memory}, Confidence: {res_confidence}")
        return response.message('0000')

    except Exception as e:
        return response.message('9999')
