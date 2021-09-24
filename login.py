from db import Database
import hashlib

class Login:
    def __init__(self):
        db = Database()
        self.db = db.db
        self.cursor = db.cursor

    def signup(self, email, password):
        self.cursor.execute('SELECT COUNT(*) FROM users WHERE email = "%s" AND password = "%s"' % (email, self.__to_sha256(password)))
        (total,) = self.cursor.fetchone()
        if total <= 0:
            self.cursor.execute('INSERT INTO users (email, password) VALUES ("%s", "%s")' % (email, self.__to_sha256(password)))
            self.db.commit()
            self.cursor.execute('SELECT * FROM users WHERE email = "%s"' % email)
            (id, email, _) = self.cursor.fetchone()
            return (id, email)
        else:
            return (None, None)
        
    def login(self, email, password):
        self.cursor.execute('SELECT * FROM users LEFT JOIN user_infos ON users.id = user_infos.user_id WHERE email = "%s" AND password = "%s"' % (email, self.__to_sha256(password)))
        (id, email, _, _, _, display_name, user_name, interests, _, _) = self.cursor.fetchone()
        if id:
            return (id, email, display_name, user_name, interests)
        else:
            return False
        
    def __to_sha256(self, password):
        return hashlib.sha256(f'{password}'.encode()).hexdigest()