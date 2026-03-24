from flask import Blueprint, request, jsonify
from flaskr.services.account_service import AccountService

transactions_bp = Blueprint('transactions', __name__)

@transactions_bp.route('/accounts/<int:account_id>/transactions', methods=['GET'])
def get_transactions(account_id):
    return jsonify(AccountService.get_transactions(account_id))