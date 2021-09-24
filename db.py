import mysql.connector

class Database:
    def __init__(self):
        self.db = mysql.connector.connect(
            host = 'localhost',
            user = 'root',
            password = '',
            database = 'twitter_development'
        )

        self.cursor = self.db.cursor()