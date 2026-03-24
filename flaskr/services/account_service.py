from flaskr import db
from flaskr.models.account import Account
from flaskr.models.transaction import Transaction
from sqlalchemy.exc import IntegrityError

class AccountService:

    @staticmethod
    def create_account(data):
        """Create a new account using the Account model."""
        try:
            account = Account.create(data)
            # Convert ObjectId to string for JSON serialization
            account['_id'] = str(account['_id'])
            account['user_id'] = str(account['user_id'])
            return account, 201
        except Exception as e:
            return {"error": str(e)}, 400   
    
    @staticmethod
    def get_account(account_id):
        account = Account.query.get(account_id)
        if not account:
            return {"error": "Account not found"}, 404
        return {"accountId": account.id, "userName": account.user.name, "balance": float(account.balance)}

    @staticmethod
    def deposit(account_id, amount):
        if amount <= 0:
            return {"error": "Deposit amount must be positive"}, 400
        account = Account.query.get(account_id)
        if not account:
            return {"error": "Account not found"}, 404
        account.balance += amount
        txn = Transaction(account_id=account_id, txn_type="DEPOSIT", amount=amount)
        db.session.add(txn)
        db.session.commit()
        return {"accountId": account.id, "balance": float(account.balance)}

    @staticmethod
    def withdraw(account_id, amount):
        if amount <= 0:
            return {"error": "Withdraw amount must be positive"}, 400
        account = Account.query.get(account_id)
        if not account:
            return {"error": "Account not found"}, 404
        if account.balance < amount:
            return {"error": "Insufficient balance"}, 400
        account.balance -= amount
        txn = Transaction(account_id=account_id, txn_type="WITHDRAW", amount=amount)
        db.session.add(txn)
        db.session.commit()
        return {"accountId": account.id, "balance": float(account.balance)}

    @staticmethod
    def get_transactions(account_id):
        account = Account.query.get(account_id)
        if not account:
            return {"error": "Account not found"}, 404
        txns = Transaction.query.filter_by(account_id=account_id).order_by(Transaction.created_at.desc()).all()
        return [
            {"type": txn.txn_type, "amount": float(txn.amount), "date": txn.created_at.strftime("%Y-%m-%d")} for txn in txns
        ]
