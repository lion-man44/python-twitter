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
            dic['profile_image'] = user_info.profile_image
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
    # def get_tweets(self, data):
    #     current_user_id = itemgetter('user_id')(data)
    #     sql = 'SELECT * FROM tweets LEFT JOIN user_infos ON tweets.user_id = user_infos.user_id \
    #         LEFT JOIN tweet_likes ON tweets.id = tweet_likes.tweet_id ORDER BY tweets.id DESC'
    #     self.cursor.execute(sql)
    #     tweets = self.cursor.fetchall()

    #     second_sql = 'SELECT * FROM followers WHERE user_id = %s' % current_user_id
    #     self.cursor.execute(second_sql)
    #     followers = self.cursor.fetchall()

    #     result = []
    #     for t in tweets:
    #         dic = {}
    #         id, user_id, message, is_visible, user_info_id, _, display_name, user_name, age, interests, profile_image, _, pushed_user_id, _ = t
    #         for f in followers:
    #             _, user_id_on_followers, follow_id = f
    #             if current_user_id == user_id_on_followers and follow_id == user_id:
    #                 dic['following'] = True
    #             else:
    #                 dic['following'] = False

    #         dic['id'] = id
    #         dic['user_id'] = user_id
    #         dic['message'] = message
    #         dic['is_visible'] = is_visible
    #         dic['user_info_id'] = user_info_id
    #         dic['display_name'] = display_name
    #         dic['user_name'] = user_name
    #         dic['age'] = age
    #         dic['interests'] = interests
    #         dic['profile_image'] = profile_image
    #         dic['pushed_user_id'] = pushed_user_id
    #         result.append(dic)

    #     return result
        
    # def add_tweet(self, data):
    #     user_id, message = itemgetter('user_id', 'message')(data)
    #     sql = 'INSERT INTO tweets (user_id, message) VALUES (%s, "%s")' % (user_id, message)
    #     self.cursor.execute(sql)
    #     self.db.commit()
        
    #     return True
    
    # def invisible_tweet(self, id):
    #     sql = 'SELECT COUNT(id) FROM tweets WHERE is_visible = 1 AND id = %s' % id
    #     self.cursor.execute(sql)
    #     total = self.cursor.fetchone()
    #     if total[0] > 0:
    #         next_sql = 'UPDATE tweets SET is_visible = 0 WHERE id = %s' % id
    #     else:
    #         next_sql = 'UPDATE tweets SET is_visible = 1 WHERE id = %s' % id

    #     self.cursor.execute(next_sql)
    #     self.db.commit()
        
    #     return True
    
    # def delete_tweet(self, id):
    #     sql = 'DELETE FROM tweets WHERE id = %s' % id
    #     self.cursor.execute(sql)
    #     self.db.commit()
        
    #     return True