from flask import render_template, request
import sqlite3
import os

# Pagination
def object_list(template_name, query, paginate_by=20, **context):
    page = request.args.get('page')
    if page and page.isdigit():
        page = int(page)
    else:
        page = 1
    
    object_list = query.paginate(page, paginate_by)
    return render_template(template_name, object_list=object_list, **context)

# Querring projects.db 
def get_portfolio_content():
    # SQLITE connection
    APP_DIR = os.getcwd()
    DATABASE_URI = os.path.join(APP_DIR, "projects.db")
    db_conn = sqlite3.connect(DATABASE_URI)
    c = db_conn.cursor()

    # Quering projects database
    c.execute("SELECT * FROM projects")
    projects = c.fetchall()
    # Close db conn
    db_conn.close()

    # Save all project to list
    projects_list = []
    # Iter through all projects
    for project in projects:
        one_project = []
        one_project.extend(project[1:])

        projects_list.append(one_project)

    return projects_list

def get_skills_content():
    # SQLITE connection
    APP_DIR = os.getcwd()
    DATABASE_URI = os.path.join(APP_DIR, "projects.db")
    db_conn = sqlite3.connect(DATABASE_URI)
    c = db_conn.cursor()

    # Quering projects database
    c.execute("SELECT * FROM skills")
    skills = c.fetchall()
    # Close db conn
    db_conn.close()

    skill_list = []
    # iterate through all the skills in the database
    for skill in skills:
        skill_one = []
        skill_one.extend(skill[1:])
        skill_list.append(skill_one)

    return skill_list