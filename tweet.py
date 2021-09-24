from db import Database
from operator import itemgetter

class Tweet:
    def __init__(self):
        db = Database()
        self.db = db.db
        self.cursor = db.cursor

    def get_tweets(self, data):
        current_user_id = itemgetter('user_id')(data)
        sql = 'SELECT * FROM tweets LEFT JOIN user_infos ON tweets.user_id = user_infos.user_id \
            LEFT JOIN tweet_likes ON tweets.id = tweet_likes.tweet_id ORDER BY tweets.id DESC'
        self.cursor.execute(sql)
        tweets = self.cursor.fetchall()

        second_sql = 'SELECT * FROM followers WHERE user_id = %s' % current_user_id
        self.cursor.execute(second_sql)
        followers = self.cursor.fetchall()

        result = []
        for t in tweets:
            dic = {}
            id, user_id, message, is_visible, user_info_id, _, display_name, user_name, age, interests, profile_image, _, pushed_user_id, _ = t
            for f in followers:
                _, user_id_on_followers, follow_id = f
                if current_user_id == user_id_on_followers and follow_id == user_id:
                    dic['following'] = True
                else:
                    dic['following'] = False

            dic['id'] = id
            dic['user_id'] = user_id
            dic['message'] = message
            dic['is_visible'] = is_visible
            dic['user_info_id'] = user_info_id
            dic['display_name'] = display_name
            dic['user_name'] = user_name
            dic['age'] = age
            dic['interests'] = interests
            dic['profile_image'] = profile_image
            dic['pushed_user_id'] = pushed_user_id
            result.append(dic)

        return result
        
    def add_tweet(self, data):
        user_id, message = itemgetter('user_id', 'message')(data)
        sql = 'INSERT INTO tweets (user_id, message) VALUES (%s, "%s")' % (user_id, message)
        self.cursor.execute(sql)
        self.db.commit()
        
        return True
    
    def invisible_tweet(self, id):
        sql = 'SELECT COUNT(id) FROM tweets WHERE is_visible = 1 AND id = %s' % id
        self.cursor.execute(sql)
        total = self.cursor.fetchone()
        if total[0] > 0:
            next_sql = 'UPDATE tweets SET is_visible = 0 WHERE id = %s' % id
        else:
            next_sql = 'UPDATE tweets SET is_visible = 1 WHERE id = %s' % id

        self.cursor.execute(next_sql)
        self.db.commit()
        
        return True
    
    def delete_tweet(self, id):
        sql = 'DELETE FROM tweets WHERE id = %s' % id
        self.cursor.execute(sql)
        self.db.commit()
        
        return True