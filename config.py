import os

# This file contains instructions for flask app


class Configuration(object):
    APP_DIR = os.path.dirname(os.path.realpath(__file__))
    DEBUG = True
    SQLALCHEMY_DATABASE_URI = 'sqlite:///%s' % os.path.join(APP_DIR, "site.db")
    SQLALCHEMY_TRACK_MODIFICATIONS = False
    SECRET_KEY = '91f3cd4f5c6b411e7c60794b3d9d31af'
