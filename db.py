import os
from flask_sqlalchemy import SQLAlchemy

class Database:
    _instance = None
    app = None
    database = None

    def __new__(klass, flask_app):
        if klass._instance is None:
            klass.app = flask_app
            klass._instance = super(Database, klass).__new__(klass)
            klass.__initialize(klass)
        return klass._instance

    def __initialize(klass):
        klass.app.config['SQLALCHEMY_DATABASE_URI'] = os.environ['SQLALCHEMY_DATABASE_URI']
        klass.app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
        klass.database = SQLAlchemy(klass.app)
