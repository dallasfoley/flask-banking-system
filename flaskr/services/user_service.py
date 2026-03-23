from flaskr import db
from flaskr.models.user import User

class UserService:

    @staticmethod
    def get_all():
        return "All users"
    @staticmethod
    def get_by_id(user_id):
        user = User.query.get_or_404(user_id)
        return "User %s" % user.name

    @staticmethod
    def create(data):
        user = User(name=data["name"], email=data["email"])
        return "Created user %s" % user.__dict__()