from flaskr import mongo
from bson.objectid import ObjectId
from datetime import datetime, timezone

class User:
    """User collection helper"""
    
    @staticmethod
    def get_collection():
        return mongo.db.users
    
    @staticmethod
    def create(data):
        """Create a new user"""
        doc = {
            'email': data['email'],
            'name': data['name'],
            'created_at': datetime.now(timezone.utc)
        }
        result = mongo.db.users.insert_one(doc)
        doc['_id'] = result.inserted_id
        return doc
    
    @staticmethod
    def find_by_id(user_id):
        """Find user by ObjectId"""
        return mongo.db.users.find_one({'_id': ObjectId(user_id)})
    
    @staticmethod
    def find_all():
        """Get all users"""
        return list(mongo.db.users.find())
    
    @staticmethod
    def update(user_id, data):
        """Update user fields"""
        update_data = {}
        if 'name' in data:
            update_data['name'] = data['name']
        if 'email' in data:
            update_data['email'] = data['email']
        if update_data:
            mongo.db.users.update_one(
                {'_id': ObjectId(user_id)},
                {'$set': update_data}
            )
        return User.find_by_id(user_id)
    
    @staticmethod
    def delete(user_id):
        """Delete user (and all their accounts and transactions)"""
        from .account import Account  # Import here to avoid circular import
        accounts = Account.find_by_user(user_id)
        for account in accounts:
            Account.delete(account['_id'])
        return mongo.db.users.delete_one({'_id': ObjectId(user_id)})