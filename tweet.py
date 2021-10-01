import os
from flask import json
from follower import Followers
from tweet_like import TweetLikes
from user_info import UserInfos
from user import Users
from db import Database

db = Database.database

class Tweets(db.Model):
    id = db.Column(db.Integer, primary_key = True)
    user_id = db.Column(db.Integer, db.ForeignKey(Users.id), unique = True)
    message = db.Column(db.String(140), nullable = True)
    is_visible = db.Column(db.Boolean, nullable = True, default = True)
    following = False

    user = db.relationship('Users', backref = 'users')
    tweet_likes = db.relationship('TweetLikes', back_populates = 'tweet')
    tweet_like = db.relationship('TweetLikes', uselist = False, back_populates = 'tweet')

    def __repr__(self):
        return '<Tweets %s, %s, %s, %s>' \
            % (self.id, self.user_id, self.message, self.is_visible)

    def __init__(self, data):
        self.user_id = data['user_id']
        self.message = data['message']

    @classmethod
    def default_tweets(self, user_id):
        tweets = Tweets.query \
            .join(UserInfos, UserInfos.user_id == Tweets.user_id) \
            .join(TweetLikes, isouter = True) \
            .order_by(db.desc(Tweets.id)) \
            .all()
        followers = Followers.query.filter_by(user_id = user_id).all()

        result = []
        for t in tweets:
            dic = {}
            for f in followers:
                if user_id == f.user_id and f.follow_id == t.user_id:
                    dic['following'] = True
                else:
                    dic['following'] = False

            dic['id'] = t.id
            dic['user_id'] = t.user_id
            dic['message'] = t.message
            dic['is_visible'] = t.is_visible
            user_info = t.user.user_info
            dic['user_info_id'] = user_info.id
            dic['display_name'] = user_info.display_name
            dic['user_name'] = user_info.user_name
            dic['age'] = user_info.age
            dic['interests'] = user_info.interests
            dic['profile_image'] = os.environ['S3_BUCKET'] + '/' + user_info.profile_image
            dic['pushed_user_id'] = t.tweet_likes[0].user_id if t.tweet_likes else 0
            result.append(dic)

        return result

    @classmethod
    def search(self, id):
        return Tweets.query.filter_by(id = id).first()

    def create(self):
        db.session.add(self)
        db.session.commit()
        return self

    def delete(self):
        db.session.delete(self)
        db.session.commit()
        return self

    def invisible(self):
        self.is_visible = not self.is_visible
        db.session.commit()
        return self

    def to_json(self):
        return json.dumps(self, default = lambda o: '', sort_keys = True, indent = 4)
