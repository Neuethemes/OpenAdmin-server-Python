from db import db

class MessageModel(db.Model):
    __tablename__ = 'messages'

    _id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(255))
    avatar = db.Column(db.String(255))
    date = db.Column(db.String(255))
    header = db.Column(db.String(255))
    content = db.Column(db.String(255))

    def __init__(self, name, avatar, date, header, content):
        self.name = name
        self.avatar = avatar
        self.date = date
        self.header = header
        self.content = content

    def json(self):
        return {
            'name': self.name,
            'avatar': self.avatar,
            'date': self.date,
            'header': self.header,
            'content': self.content
        }

    @classmethod
    def find_by_name(cls, name):
        return cls.query.filter_by(name=name).first()

    def save_to_db(self):
        db.session.add(self)
        db.session.commit()

    def delete_from_db(self):
        db.session.delete(self)
        db.session.commit()
