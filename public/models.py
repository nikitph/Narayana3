from extensions import db


class Thought(db.Document):
    dys_thought = db.StringField(required=True)
    user = db.StringField(required=True)
    rational = db.StringField(required=False)
    distress = db.IntField(required=True)
    distortion = db.StringField(required=True)


class User(db.Document):
    phone = db.IntField(required=True)
    pin = db.IntField(required=True)