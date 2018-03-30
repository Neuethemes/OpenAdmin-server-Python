import datetime, configparser

from flask import Flask, jsonify
from flask_restful import Api
from flask_jwt import JWT
from flask_cors import CORS

from security import authenticate, identity as identity_function
from resources.user import UserRegister
from resources.messages import Message, MessageList
from resources.stats import Stats

config = configparser.ConfigParser()
config.read('config.ini')

app = Flask(__name__)

app.config['SQLALCHEMY_DATABASE_URI'] = config['DEFAULT']['SQLALCHEMY_DATABASE_URI']
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = config['DEFAULT'].getboolean('SQLALCHEMY_TRACK_MODIFICATIONS')

app.config['JWT_AUTH_URL_RULE'] = config['DEFAULT']['JWT_AUTH_URL_RULE']
app.config['JWT_AUTH_USERNAME_KEY'] = config['DEFAULT']['JWT_AUTH_USERNAME_KEY']
app.config['JWT_EXPIRATION_DELTA'] = datetime.timedelta(days=config.getint('DEFAULT', 'JWT_EXPIRATION_DELTA'))

app.secret_key = config['DEFAULT']['SECRET_KEY']

CORS(app)
api = Api(app)

jwt = JWT(app, authenticate, identity_function)

@jwt.auth_response_handler
def customized_response_handler(access_token, identity):
    return jsonify({
        'access_token': access_token.decode('utf-8'),
        'user_id': identity.id,
        'user_email': identity.email
    })

api.add_resource(Stats, '/stats/<string:type>')
api.add_resource(Message, '/message/<string:name>')
api.add_resource(MessageList, '/messages')
api.add_resource(UserRegister, '/user/register')

if __name__ == '__main__':
    from db import db
    db.init_app(app)
    app.run(port=config.getint('DEFAULT', 'APP_PORT'), debug=config['DEFAULT'].getboolean('APP_DEBUG'))
