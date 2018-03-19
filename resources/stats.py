from flask_restful import Resource, reqparse
from flask_jwt import jwt_required
from models.stats import StatsModel

class Stats(Resource):
    parser = reqparse.RequestParser()

    @jwt_required()
    def get(self, type):
        stats = StatsModel.find_by_type(type)
        if stats:
            return stats.json()
        return {'message': 'Item not found'}, 404
