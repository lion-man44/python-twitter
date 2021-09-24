from db import Database

class TweetLike:
    def __init__(self):
        db = Database()
        self.db = db.db
        self.cursor = db.cursor


    def favorite(self, id, pushed_user_id):
        sql = 'SELECT COUNT(id) FROM tweet_likes WHERE user_id = %s AND tweet_id = %s' % (pushed_user_id, id)
        self.cursor.execute(sql)
        total = self.cursor.fetchone()
        if (total[0] > 0):
            next_sql = 'DELETE FROM tweet_likes WHERE user_id = %s AND tweet_id = %s' % (pushed_user_id, id)
        else:
            next_sql = 'INSERT INTO tweet_likes (user_id, tweet_id) VALUES (%s, %s)' % (pushed_user_id, id)

        self.cursor.execute(next_sql)
        self.db.commit()

        return True