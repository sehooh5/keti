from flask import Blueprint, request, jsonify

user_bp = Blueprint('user_bp', __name__)

@user_bp.route('/<int:user_id>/followers', methods=['GET'])
def get_followers(user_id):
    # Get followers logic here
    return jsonify({"message": "List of followers"})

@user_bp.route('/<int:user_id>/followings', methods=['GET'])
def get_followings(user_id):
    # Get followings logic here
    return jsonify({"message": "List of followings"})

@user_bp.route('/<int:user_id>/follow', methods=['POST'])
def follow_user(user_id):
    # Follow user logic here
    return jsonify({"message": "User followed"}), 201
