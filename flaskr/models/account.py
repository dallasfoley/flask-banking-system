from flaskr import mongo
from bson.objectid import ObjectId
from datetime import datetime, timezone

class Account:
    """Account collection helper"""
    
    @staticmethod
    def get_collection():
        return mongo.db.accounts
    
    @staticmethod
    def create(data):
        """Create a new account"""
        doc = {
            'user_id': ObjectId(data['user_id']),  # reference to User
            'balance': float(data.get('balance', 0.0)),
            'account_type': data['account_type'],
            'created_at': datetime.now(timezone.utc)
        }
        result = mongo.db.accounts.insert_one(doc)
        doc['_id'] = result.inserted_id
        return doc
    
    @staticmethod
    def find_by_id(account_id):
        """Find account by ObjectId"""
        return mongo.db.accounts.find_one({'_id': ObjectId(account_id)})
    
    @staticmethod
    def find_by_user(user_id):
        """Find all accounts belonging to a user"""
        return list(mongo.db.accounts.find({'user_id': ObjectId(user_id)}))
    
    @staticmethod
    def update_balance(account_id, new_balance):
        """Update account balance"""
        mongo.db.accounts.update_one(
            {'_id': ObjectId(account_id)},
            {'$set': {'balance': new_balance}}
        )
        return Account.find_by_id(account_id)
    
    @staticmethod
    def delete(account_id):
        """Delete account (and all its transactions – handle separately if needed)"""
        # Optionally delete related transactions
        from .transaction import Transaction
        Transaction.delete_by_account(account_id)
        return mongo.db.accounts.delete_one({'_id': ObjectId(account_id)})