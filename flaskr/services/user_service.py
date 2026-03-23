from flaskr import db
from flaskr.models.user import User

class UserService:
    @staticmethod
    def get_by_id(user_id):
        user = User.query.get_or_404(user_id)
        return {"id": user.id, "name": user.name, "email": user.email}

    @staticmethod
    def create(data):
        user = User(name=data["name"], email=data["email"])
        db.session.add(user)
        db.session.commit()
        return {"id": user.id, "name": user.name, "email": user.email}