from flask import render_template, request
import sqlite3
import os

def object_list(template_name, query, paginate_by=20, **context):
    page = request.args.get('page')
    if page and page.isdigit():
        page = int(page)
    else:
        page = 1
    
    object_list = query.paginate(page, paginate_by)
    return render_template(template_name, object_list=object_list, **context)

def get_portfolio_content():
    '''
    Function to get all porfolio projects from database
    '''
    # Reestablish database
    APP_DIR = '/Users/jonaslaurinaitis/Desktop/core/projectsFlask/my_resume'
    PROJECTS_DATABASE_URI = os.path.join(APP_DIR, "projects.db")
    conn = sqlite3.connect(PROJECTS_DATABASE_URI)
    cur = conn.cursor()

    # Select all projects from database
    cur.execute("SELECT * FROM portfolio")
    projects = cur.fetchall()
    # Close connection
    conn.close()
    