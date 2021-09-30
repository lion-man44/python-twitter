from user_info import UserInfos
from user import Users

class Login:
    def __init__(self):
        pass

    def signup(self, email, password):
        exists_user = Users.search({ 'email': email, 'password': password})
        if exists_user:
            return exists_user
        else:
            u = Users({ 'email': email, 'password': password })
            created_user = u.create()
            UserInfos.initial_to_create(created_user.id)
            return created_user

    def login(self, email, password):
        exists_user = Users.search({ 'email': email, 'password': password})
        if exists_user:
            return exists_user
        else:
            return None
