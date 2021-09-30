from flask import json
from user import Users
from db import Database

db = Database.database

class Followers(db.Model):
    id = db.Column(db.Integer, primary_key = True)
    user_id = db.Column(db.Integer, db.ForeignKey(Users.id), nullable = True)
    follow_id = db.Column(db.Integer, db.ForeignKey(Users.id), nullable = True)

    def __init__(self, data):
        self.user_id = data['user_id']
        self.follow_id = data['follow_id']

    @classmethod
    def search(self, data):
        return Followers.query.filter_by(user_id = data['user_id'], follow_id = data['follow_id']).first()

    def create(self):
        db.session.add(self)
        db.session.commit()
        return self

    def delete(self):
        db.session.delete(self)
        db.session.commit()
        return self

    def to_json(self):
        return json.dumps(self, default = lambda o: '', sort_keys = True, indent = 4)
