from user import Users
from db import Database

db = Database.database

class UserInfos(db.Model):
    id = db.Column(db.Integer, primary_key = True)
    user_id = db.Column(db.Integer, db.ForeignKey(Users.id), unique = True)
    display_name = db.Column(db.String(80))
    user_name = db.Column(db.String(80))
    age = db.Column(db.Integer, default = 0)
    interests = db.Column(db.String(256))
    profile_image = db.Column(db.String(256), nullable = False, default = '150x150.png')

    user = db.relationship('Users', uselist = False, foreign_keys = 'UserInfos.user_id')

    def __repr__(self):
        return '<UserInfos %s, %s, %s, %s, %s, %s, %s>' \
            % (self.id, self.user_id, self.display_name, self.user_name, self.age, self.interests, self.profile_image)

    def __init__(self, data):
        self.user_id = data['user_id']
        if 'display_name' in data:
            self.display_name = data['display_name']
        if 'user_name' in data:
            self.user_name = data['user_name']
        if 'age' in data:
            self.age = data['age']
        if 'interests' in data:
            self.interests = data['interests']
        if 'profile_image' in data:
            self.profile_image = data['profile_image']

    @classmethod
    def initial_to_create(self, user_id):
        u = UserInfos({ 'user_id': user_id })
        return u.create()

    @classmethod
    def search(self, data):
        return UserInfos.query.filter_by(user_id = data['user_id']).limit(1).first()

    def create(self):
        db.session.add(self)
        db.session.commit()
        return self

    def update(self, data):
        if 'display_name' in data:
            self.display_name = data['display_name']
        if 'user_name' in data:
            self.user_name = data['user_name']
        if 'age' in data:
            self.age = data['age']
        if 'interests' in data:
            self.interests = data['interests']

        if 'email' in data:
            self.user.update({ 'email': data['email'] })

        db.session.commit()
        return self
    
    def upload_image(self, filename):
        self.profile_image = filename

        db.session.commit()
        return self

    def get_image(self):
        return self.profile_image