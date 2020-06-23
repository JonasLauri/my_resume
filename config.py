import os

# This file contains instructions for flask app
class Configuration(object):
    APP_DIR = os.path.dirname(os.path.realpath(__file__))
    DEBUG = True
    SQLALCHEMY_DB_URI = 'sqliteext:///%s' % os.path.join(APP_DIR, "site.db")
