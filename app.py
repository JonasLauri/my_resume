from flask import (Flask, render_template, url_for, flash, redirect, abort,
                    request, Response, session, Markup)
from flask_migrate import Migrate, MigrateCommand
from flask_script import Manager
from flask_moment import Moment
from flask_sqlalchemy import SQLAlchemy

from config import Configuration


# App initialization
app = Flask(__name__)
app.config.from_object(Configuration)

# For date and time formating
moment = Moment(app)


# Init sqlalchemy for managing db
db = SQLAlchemy(app)
import models

migrate = Migrate(app, db)
manager = Manager(app)
manager.add_command('db', MigrateCommand)

# SECRET_KEY = '91f3cd4f5c6b411e7c60794b3d9d31af'


