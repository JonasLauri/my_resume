from app import app
from flask import (Flask, render_template, url_for, flash, redirect, abort,
                    request, Response, session, Markup)
import helpers

# Views module
# App routes
@app.route('/')
@app.route('/home')
def index():
    return render_template('/home.html')

@app.route('/about')
def about():
    return render_template('/about.html')

@app.route('/portfolio', methods=['POST', 'GET'])
def portfolio():
    projects = helpers.get_portfolio_content()
    # Make list of lists always even
    if len(projects) % 2 == 0:
        pass
    else:
        projects.append(['Additional_list'])

    # Make iterable object
    iterator = iter(projects)
    # Aggregate two projects in zip 
    zipped = zip(iterator, iterator)
    
    return render_template('/portfolio.html', title='Projects - Jonas Laurinaitis', projects=zipped)
