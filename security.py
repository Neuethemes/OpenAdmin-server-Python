from models.user import UserModel
from flask_bcrypt import Bcrypt

def authenticate(email, password):
    user = UserModel.find_by_email(email)

    bcrypt = Bcrypt()
    if user and bcrypt.check_password_hash(user.password, password):
        return user

def identity(payload):
    user_id = payload['identity']
    return UserModel.find_by_id(user_id)
