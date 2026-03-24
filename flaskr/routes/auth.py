from flask import Blueprint, request, jsonify
from flask_jwt_extended import (
    create_access_token, create_refresh_token,
    jwt_required, get_jwt_identity
)
from flaskr import limiter
from ..services.user_service import UserService

auth_bp = Blueprint('auth', __name__)

@auth_bp.route('/login', methods=['POST'])
# @limiter.limit("10 per minute")  # brute-force protection
def login():
    data = request.json or {}
    email = data.get('email')
    password = data.get('password')

    if not email or not password:
        return jsonify({"error": "Email and password are required"}), 400

    user = UserService.authenticate(email, password)
    if not user:
        return jsonify({"error": "Invalid credentials"}), 401  # never say which field is wrong

    user_id = str(user['_id'])
    return jsonify({
        "accessToken":  create_access_token(identity=user_id),
        "refreshToken": create_refresh_token(identity=user_id)
    }), 200

@auth_bp.route('/refresh', methods=['POST'])
@jwt_required(refresh=True)
def refresh():
    user_id = get_jwt_identity()
    return jsonify({"accessToken": create_access_token(identity=user_id)}), 200