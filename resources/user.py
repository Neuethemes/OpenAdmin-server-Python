from flask_restful import Resource, reqparse
from flask_bcrypt import Bcrypt
from models.user import UserModel

class UserRegister(Resource):

    parser = reqparse.RequestParser()
    parser.add_argument('email',
        type=str,
        required=True,
        help="This field cannot be blank."
    )
    parser.add_argument('password',
        type=str,
        required=True,
        help="This field cannot be blank."
    )

    def post(self):
        data = UserRegister.parser.parse_args()

        if UserModel.find_by_email(data['email']):
            return {"message": "A user with that email already exists"}, 400

        bcrypt = Bcrypt()
        data['password'] = bcrypt.generate_password_hash(data['password'], 10).decode('utf-8')

        user = UserModel(data['email'], data['password'])
        user.save_to_db()

        return {"message": "User created successfully."}, 201
