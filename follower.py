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

    # def follow(self, user_id, follow_id):
    #     sql = 'SELECT COUNT(id) FROM followers WHERE user_id = %s AND follow_id = %s' % (user_id, follow_id)
    #     self.cursor.execute(sql)
    #     total = dict(zip(self.cursor.column_names, self.cursor.fetchone()))
    #     if total['COUNT(id)'] > 0:
    #         return False
    #     else:
    #         next_sql = 'INSERT INTO followers (user_id, follow_id) VALUES (%s, %s)' % (user_id, follow_id)

    #     self.cursor.execute(next_sql)
    #     self.db.commit()
    #     return True

    # def unfollow(self, user_id, follow_id):
    #     sql = 'DELETE FROM followers WHERE user_id = %s AND follow_id = %s' % (user_id, follow_id)
    #     self.cursor.execute(sql)
    #     self.db.commit()

    #     return True