from flask import Blueprint, request, jsonify
from ..services.user_service import UserService

users_bp = Blueprint('users', __name__)

@users_bp.route('/', methods=['GET'])
def get_all_users():
    return jsonify(UserService.get_all())

@users_bp.route('/', methods=['POST'])
def create_user():
    return jsonify(UserService.create_user(request.json)), 201

@users_bp.route('/<user_id>', methods=['GET'])
def get_user(user_id):
    return jsonify(UserService.get_by_id(user_id))