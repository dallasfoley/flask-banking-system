from flaskr import mongo
from flaskr.models.account import Account
from flaskr.models.transaction import Transaction
from bson.objectid import ObjectId
from bson.errors import InvalidId

class AccountService:

    @staticmethod
    def create_account(data):
        try:
            account = Account.create(data)
            account['_id'] = str(account['_id'])
            account['user_id'] = str(account['user_id'])
            return account, 201
        except KeyError as e:
            return {"error": f"Missing required field: {e}"}, 400
        except Exception as e:
            return {"error": str(e)}, 400

    @staticmethod
    def get_account(account_id):
        try:
            account = Account.find_by_id(account_id)
        except InvalidId:
            return {"error": "Invalid account ID"}, 400
        if not account:
            return {"error": "Account not found"}, 404
        return {
            "accountId": str(account['_id']),
            "userId": str(account['user_id']),
            "accountType": account['account_type'],
            "balance": account['balance']
        }, 200

    @staticmethod
    def deposit(account_id, amount):
        if not isinstance(amount, (int, float)) or amount <= 0:
            return {"error": "Deposit amount must be a positive number"}, 400
        try:
            account = Account.find_by_id(account_id)
        except InvalidId:
            return {"error": "Invalid account ID"}, 400
        if not account:
            return {"error": "Account not found"}, 404

        new_balance = account['balance'] + amount
        updated = Account.update_balance(account_id, new_balance)
        Transaction.create({
            'account_id': account_id,
            'txn_type': 'DEPOSIT',
            'amount': amount
        })
        return {"accountId": str(updated['_id']), "balance": updated['balance']}, 200

    @staticmethod
    def withdraw(account_id, amount):
        if not isinstance(amount, (int, float)) or amount <= 0:
            return {"error": "Withdraw amount must be a positive number"}, 400
        try:
            account = Account.find_by_id(account_id)
        except InvalidId:
            return {"error": "Invalid account ID"}, 400
        if not account:
            return {"error": "Account not found"}, 404
        if account['balance'] < amount:
            return {"error": "Insufficient balance"}, 400

        new_balance = account['balance'] - amount
        updated = Account.update_balance(account_id, new_balance)
        Transaction.create({
            'account_id': account_id,
            'txn_type': 'WITHDRAW',
            'amount': amount
        })
        return {"accountId": str(updated['_id']), "balance": updated['balance']}, 200

    @staticmethod
    def get_transactions(account_id):
        try:
            account = Account.find_by_id(account_id)
        except InvalidId:
            return {"error": "Invalid account ID"}, 400
        if not account:
            return {"error": "Account not found"}, 404

        txns = Transaction.find_by_account(account_id)
        return [
            {
                "type": txn['txn_type'],
                "amount": txn['amount'],
                "date": txn['created_at'].strftime("%Y-%m-%d")
            }
            for txn in txns
        ], 200