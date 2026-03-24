from flaskr import mongo
from bson.objectid import ObjectId
from datetime import datetime, timezone

class Transaction:
    """Transaction collection helper"""
    
    @staticmethod
    def get_collection():
        return mongo.db.transactions
    
    @staticmethod
    def create(data):
        """Create a new transaction"""
        doc = {
            'account_id': ObjectId(data['account_id']),
            'txn_type': data['txn_type'],  # DEPOSIT or WITHDRAW
            'amount': float(data['amount']),
            'created_at': datetime.now(timezone.utc)
        }
        result = mongo.db.transactions.insert_one(doc)
        doc['_id'] = result.inserted_id
        return doc
    
    @staticmethod
    def find_by_account(account_id):
        """Find all transactions for an account, sorted by date descending"""
        return list(mongo.db.transactions.find(
            {'account_id': ObjectId(account_id)}
        ).sort('created_at', -1))
    
    @staticmethod
    def delete_by_account(account_id):
        """Delete all transactions for a given account"""
        mongo.db.transactions.delete_many({'account_id': ObjectId(account_id)})