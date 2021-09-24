from operator import itemgetter
from user import User
from db import Database

class UserInfo:
    def __init__(self):
        db = Database()
        self.db = db.db
        self.cursor = db.cursor

    def get_user_info(self, user_id):
        self.cursor.execute('SELECT * FROM users LEFT JOIN user_infos ON users.id = user_infos.user_id WHERE users.id = %s' % user_id)
        (id, email, _, user_info_id, _, display_name, user_name, interests, profile_image, age) = self.cursor.fetchone()
        return (id, email, user_info_id, display_name, user_name, interests, profile_image, age)

    def get_profile_image(self, user_id):
        sql = 'SELECT profile_image FROM user_infos WHERE user_id = %s' % user_id
        self.cursor.execute(sql)
        profile_image = self.cursor.fetchone()
        return profile_image

    def insert_user_info(self, data):
        user_id, display_name, user_name, age, interests = itemgetter('user_id', 'display_name', 'user_name', 'age', 'interests')(data)
        sql = 'INSERT INTO user_infos (user_id, display_name, user_name, interests, age) VALUES (%s, "%s", "%s", "%s", %s);' \
            % (user_id, self.__xstr(display_name), self.__xstr(user_name), self.__xstr(interests), age)
        self.cursor.execute(sql)
        self.db.commit()
        return True

    def update_profile_image(self, user_id, filename):
        sql = 'UPDATE user_infos SET profile_image = "%s" WHERE user_id = %s' % (filename, user_id)
        self.cursor.execute(sql)
        self.db.commit()
        return True

    def update_user_info(self, data):
        sqls = ['UPDATE user_infos SET ']
        user_id, display_name, user_name, age, email, interests = itemgetter('id', 'display_name', 'user_name', 'age', 'email', 'interests')(data)
        display_name = display_name or ''
        user_name = user_name or ''
        interests = interests or ''
        # if display_name is not None:
        sqls.append('display_name = "%s"' % self.__xstr(display_name))
        # if user_name is not None:
        sqls.append('user_name = "%s"' % self.__xstr(user_name))
        sqls.append('age = %s' % age)
        # if interests is not None:
        sqls.append('interests = "%s"' % self.__xstr(interests))

        sql = ''
        for x in range(len(sqls)):
            if x == 0 or x == (len(sqls) - 1):
                sql += sqls[x] + ' '
            else:
                sql += sqls[x] + ', '

        sql += 'WHERE user_id = %s' % user_id
        self.cursor.execute(sql)
        self.db.commit()
        if email is not None and email != '':
            u = User()
            u.update_user(user_id, email)
        
        return True
    
    def __xstr(self, s):
        return '' if s is None else str(s)