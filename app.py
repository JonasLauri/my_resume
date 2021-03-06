from flask import (Flask, render_template, url_for, flash, redirect, abort,
                    request, Response, session, Markup)
from flask_migrate import Migrate, MigrateCommand
from flask_script import Manager
from flask_sqlalchemy import SQLAlchemy

from config import Configuration


# App initialization with inherit configurations
app = Flask(__name__)
app.config.from_object(Configuration)

# Init sqlalchemy for managing db
db = SQLAlchemy(app)
import models

migrate = Migrate(app, db)
manager = Manager(app)
manager.add_command('db', MigrateCommand)