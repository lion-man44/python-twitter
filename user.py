from db import Database

class User:
    def __init__(self):
        db = Database()
        self.db = db.db
        self.cursor = db.cursor

    def update_user(self, id, email):
        self.cursor.execute('UPDATE users SET email = "%s" WHERE id = %s' % (email, id))
        self.db.commit()
        
        return True