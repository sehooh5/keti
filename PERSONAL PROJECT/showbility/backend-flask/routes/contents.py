from flask import Blueprint, request, jsonify

content_bp = Blueprint('content_bp', __name__)

@content_bp.route('/<int:group_id>/contents', methods=['GET', 'POST'])
def group_contents(group_id):
    if request.method == 'GET':
        # Get contents logic here
        return jsonify({"message": "List of contents"})
    elif request.method == 'POST':
        # Create content logic here
        return jsonify({"message": "Content created"}), 201

@content_bp.route('/<int:group_id>/contents/<int:pk>', methods=['DELETE'])
def delete_content(group_id, pk):
    # Delete content logic here
    return jsonify({"message": "Content deleted"}), 204
