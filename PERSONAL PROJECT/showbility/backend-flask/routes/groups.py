from flask import Blueprint, request, jsonify

group_bp = Blueprint('group_bp', __name__)

@group_bp.route('/<int:group_id>/members', methods=['GET', 'POST'])
def group_members(group_id):
    if request.method == 'GET':
        # Get group members logic here
        return jsonify({"message": "List of group members"})
    elif request.method == 'POST':
        # Add member logic here
        return jsonify({"message": "Member added"}), 201

@group_bp.route('/<int:group_id>/members/<int:pk>', methods=['DELETE'])
def delete_member(group_id, pk):
    # Delete member logic here
    return jsonify({"message": "Member deleted"}), 204
