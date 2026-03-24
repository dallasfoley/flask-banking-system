from flaskr import mongo
from flaskr.models.user import User
from bson.objectid import ObjectId
from bson.errors import InvalidId

class UserService:

    @staticmethod
    def get_all():
        users = User.find_all()
        # Convert ObjectId and datetime to JSON-serializable formats
        for u in users:
            u['_id'] = str(u['_id'])
            u['created_at'] = u['created_at'].isoformat()
        return users

    @staticmethod
    def get_by_id(user_id):
        try:
            user = User.find_by_id(user_id)
        except InvalidId:
            return {"error": "Invalid user ID"}, 400

        if not user:
            return {"error": "User not found"}, 404

        user['_id'] = str(user['_id'])
        user['created_at'] = user['created_at'].isoformat()
        return user

    @staticmethod
    def create_user(data):
        # Validate required fields
        if not data.get('name') or not data.get('email'):
            return {"error": "Name and email are required"}, 400

        # Check if email already exists (will be caught by unique index, but we can also check manually)
        existing = mongo.db.users.find_one({'email': data['email']})
        if existing:
            return {"error": "Email already exists"}, 409

        try:
            user = User.create(data)
        except Exception as e:
            # Handle duplicate key error from unique index
            if 'E11000' in str(e):
                return {"error": "Email already exists"}, 409
            return {"error": str(e)}, 500

        user['_id'] = str(user['_id'])
        user['created_at'] = user['created_at'].isoformat()
        return user

    @staticmethod
    def update_user(user_id, data):
        try:
            user = User.find_by_id(user_id)
        except InvalidId:
            return {"error": "Invalid user ID"}, 400

        if not user:
            return {"error": "User not found"}, 404

        # Only allow updating name and email
        allowed = ['name', 'email']
        update_data = {k: v for k, v in data.items() if k in allowed}
        if not update_data:
            return {"error": "No valid fields to update"}, 400

        # If email is being updated, check for duplicates
        if 'email' in update_data:
            existing = mongo.db.users.find_one({'email': update_data['email']})
            if existing and existing['_id'] != ObjectId(user_id):
                return {"error": "Email already taken"}, 409

        try:
            updated_user = User.update(user_id, update_data)
        except Exception as e:
            if 'E11000' in str(e):
                return {"error": "Email already exists"}, 409
            return {"error": str(e)}, 500

        updated_user['_id'] = str(updated_user['_id'])
        updated_user['created_at'] = updated_user['created_at'].isoformat()
        return updated_user

    @staticmethod
    def delete_user(user_id):
        try:
            user = User.find_by_id(user_id)
        except InvalidId:
            return {"error": "Invalid user ID"}, 400

        if not user:
            return {"error": "User not found"}, 404

        # Delete user (cascades to accounts and transactions via the model's delete)
        result = User.delete(user_id)
        if result.deleted_count == 0:
            return {"error": "User not found"}, 404

        return {"message": "User deleted successfully"}, 200