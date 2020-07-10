from app import app
from flask import (Flask, render_template, url_for, flash, redirect, abort,
                    request, Response, session, Markup)

# Views module
# App routes
@app.route('/')
@app.route('/home')
def index():
    return render_template('/home.html')

@app.route('/about')
def about():
    return render_template('/about.html')

@app.route('/portfolio')
def portfolio():
    return render_template('/portfolio.html', title='Projects - Jonas Laurinaitis')
