from flask import Blueprint, request, jsonify
from flaskr.services.account_service import AccountService

accounts_bp = Blueprint('accounts', __name__)

@accounts_bp.route('/', methods=['POST'])
def create_account():
    data = request.json
    return jsonify(AccountService.create_account(data)), 201

@accounts_bp.route('/<account_id>', methods=['GET'])
def get_account(account_id):
    return jsonify(AccountService.get_account(account_id))

@accounts_bp.route('/<account_id>/deposit', methods=['POST'])
def deposit(account_id):
    data = request.json
    amount = data.get('amount')
    return jsonify(AccountService.deposit(account_id, amount))

@accounts_bp.route('/<account_id>/withdraw', methods=['POST'])
def withdraw(account_id):
    data = request.json
    amount = data.get('amount')
    return jsonify(AccountService.withdraw(account_id, amount))

@accounts_bp.route('/<account_id>/transactions', methods=['GET'])
def get_transactions(account_id):
    return jsonify(AccountService.get_transactions(account_id))