from db import Database

class Follower:
    def __init__(self):
        db = Database()
        self.db = db.db
        self.cursor = db.cursor

    def follow(self, user_id, follow_id):
        sql = 'SELECT COUNT(id) FROM followers WHERE user_id = %s AND follow_id = %s' % (user_id, follow_id)
        self.cursor.execute(sql)
        total = dict(zip(self.cursor.column_names, self.cursor.fetchone()))
        if total['COUNT(id)'] > 0:
            return False
        else:
            next_sql = 'INSERT INTO followers (user_id, follow_id) VALUES (%s, %s)' % (user_id, follow_id)

        self.cursor.execute(next_sql)
        self.db.commit()
        return True

    def unfollow(self, user_id, follow_id):
        sql = 'DELETE FROM followers WHERE user_id = %s AND follow_id = %s' % (user_id, follow_id)
        self.cursor.execute(sql)
        self.db.commit()

        return True