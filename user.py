from db import Database
import hashlib

db = Database.database

class Users(db.Model):
    id = db.Column(db.Integer, primary_key = True)
    email = db.Column(db.String(256), unique = True, nullable = True)
    password = db.Column(db.String(256), unique = True, nullable = True)

    user_info = db.relationship('UserInfos', uselist = False, back_populates = 'user')

    def __repr__(self):
        return '<User %s, %s, %s>' % (self.id, self.email, self.password)

    def __init__(self, data):
        self.email = data['email']
        self.password = self.__to_sha256(data['password'])

    @classmethod
    def search(self, data):
        return Users.query.filter_by(email = data['email'], password = self.__to_sha256(self, data['password'])).limit(1).first()

    @classmethod
    def search_and_user_infos(self, data):
        return Users.query.filter_by(email = data['email'], password = self.__to_sha256(self, data['password'])).limit(1).first()

    def create(self):
        db.session.add(self)
        db.session.commit()
        return self

    def update(self, data):
        if 'email' in data and data['email'] != '':
            self.email = data['email']
        if 'password' in data:
            self.password = self.__to_sha256(data['password'])
        db.session.commit()
        return self

    def update_user(self, id, email):
        self.cursor.execute('UPDATE users SET email = "%s" WHERE id = %s' % (email, id))
        self.db.commit()

        return True

    def __to_sha256(self, password):
        return hashlib.sha256(f'{password}'.encode()).hexdigest()