from flask import (Flask, render_template, url_for, flash, redirect, abort,
                    request, Response, session, Markup)
from flask_sqlalchemy import SQLAlchemy

from config import Configuration


# App initialization
app = Flask(__name__)
app.config.from_object(Configuration)

# Init sqlalchemy for managing db
db = SQLAlchemy(app)


# SECRET_KEY = '91f3cd4f5c6b411e7c60794b3d9d31af'

