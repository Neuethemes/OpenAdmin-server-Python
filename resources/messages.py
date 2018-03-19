from flask_restful import Resource, reqparse
from flask_jwt import jwt_required
from models.message import MessageModel

class Message(Resource):
    parser = reqparse.RequestParser()

    @jwt_required()
    def get(self, name):
        message = MessageModel.find_by_name(name)
        if message:
            return message.json()
        return {'message': 'Item not found'}, 404

    def post(self, name):
        if MessageModel.find_by_name(name):
            return {'message': "An item with name '{}' already exists.".format(name)}, 400

        data = Message.parser.parse_args()

        message = MessageModel(name, data['avatar'], data['date'], data['header'], data['content'])

        try:
            message.save_to_db()
        except:
            return {"message": "An error occurred inserting the item."}, 500

        return message.json(), 201

    def delete(self, name):
        message = MessageModel.find_by_name(name)
        if message:
            message.delete_from_db()

        return {'message': 'Item deleted'}

class MessageList(Resource):
    @jwt_required()
    def get(self):
        return {'messages': list(map(lambda x: x.json(), MessageModel.query.all()))}
