from db import db

class StatsModel(db.Model):
    __tablename__ = 'stats'

    _id = db.Column(db.Integer, primary_key=True)
    type = db.Column(db.String(255))
    data = db.Column(db.JSON(9000))

    def __init__(self, type, data):
        self.type = type
        self.data = data

    def json(self):
        return {
            'type': self.type,
            'data': self.data,
        }

    @classmethod
    def find_by_type(cls, type):
        return cls.query.filter_by(type=type).first()

    def save_to_db(self):
        db.session.add(self)
        db.session.commit()

    def delete_from_db(self):
        db.session.delete(self)
        db.session.commit()
