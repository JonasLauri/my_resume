import pandas as pd 
import sqlite3
import os

# Read excel files to dataframes
projects_df = pd.read_excel('projects/portfolio_db.xlsx', header=0)
skills_df = pd.read_excel('projects/skills_db.xlsx', header=0)

# SQLITE connection
APP_DIR = os.path.dirname(os.path.realpath(__file__))
DATABASE_URI = os.path.join(APP_DIR, "projects.db")
db_conn = sqlite3.connect(DATABASE_URI)
c = db_conn.cursor()

# PROJECTS TABLE
c.execute("""CREATE TABLE IF NOT EXISTS projects(
    id integer PRIMARY KEY,
    title text NOT NULL,
    description text,
    skills text,
    image_url text,
    code_url text,
    date text,
    categories text
);""")

# SKILLS TABLE
c.execute(""" CREATE TABLE IF NOT EXISTS skills(
    id integer PRIMARY KEY,
    topic text,
    skills text,
    level integer,
    tooltip text
);""")

def add_data_projects():
    # Delete projects table rows
    c.execute("""DELETE FROM projects;""")

    # SQL statment
    sql = """ INSERT INTO projects(title, description, skills, image_url, code_url, date, categories) 
        VALUES(?,?,?,?,?,?,?) """
    
    # Iteration through dataframe
    projects = []
    for project_row in projects_df.itertuples():
        projects.append(tuple([ project_row.title,
           project_row.description,
           project_row.skills,
           project_row.image_url,
           project_row.code_url,
           project_row.date,
           project_row.categories]))

    # Data insertion
    c.executemany(sql, projects)
    db_conn.commit()


def add_data_skills():
    # Delete projects table rows
    c.execute("""DELETE FROM skills;""")

    # Write records from dataframe to sqlite database   
    skills_df.to_sql('skills', db_conn, if_exists='append', index=False)
    

# Run SQL commands
add_data_projects()
add_data_skills()
db_conn.close()