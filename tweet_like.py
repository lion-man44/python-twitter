from flask import json
from user import Users
from db import Database

db = Database.database

class TweetLikes(db.Model):
    id = db.Column(db.Integer, primary_key = True)
    user_id = db.Column(db.Integer, db.ForeignKey(Users.id), nullable = True)
    tweet_id = db.Column(db.Integer, db.ForeignKey('tweets.id'), nullable = True)

    user = db.relationship('Users', backref = 'user')
    tweet = db.relationship('Tweets', uselist = False, back_populates = 'tweet_likes')

    def __repr__(self):
        return '<TweetLikes %s, %s, %s>' % (self.id, self.user_id, self.tweet_id)

    def __init__(self, data):
        self.user_id = data['user_id']
        self.tweet_id = data['tweet_id']

    @classmethod
    def search(self, data):
        return TweetLikes.query.filter_by(user_id = data['user_id'], tweet_id = data['tweet_id']).first()

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

    # def favorite(self, id, pushed_user_id):
    #     sql = 'SELECT COUNT(id) FROM tweet_likes WHERE user_id = %s AND tweet_id = %s' % (pushed_user_id, id)
    #     self.cursor.execute(sql)
    #     total = self.cursor.fetchone()
    #     if (total[0] > 0):
    #         next_sql = 'DELETE FROM tweet_likes WHERE user_id = %s AND tweet_id = %s' % (pushed_user_id, id)
    #     else:
    #         next_sql = 'INSERT INTO tweet_likes (user_id, tweet_id) VALUES (%s, %s)' % (pushed_user_id, id)

    #     self.cursor.execute(next_sql)
    #     self.db.commit()

    #     return True