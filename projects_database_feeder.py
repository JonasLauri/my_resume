import pandas as pd
import numpy as np 
import sqlite3
import os

# Read excel files
projects_df = pd.read_excel("projects/portfolio_db.xlsx")

# Database connection and tables creation
APP_DIR = os.path.dirname(os.path.realpath(__file__))
PROJECTS_DATABASE_URI = os.path.join(APP_DIR, "projects.db")
conn = sqlite3.connect(PROJECTS_DATABASE_URI)
cur = conn.cursor()

# Portfolio table
cur.execute(
    """
    CREATE TABLE IF NOT EXISTS portfolio (
        id INTEGER,
        title TEXT NOT NULL,
        description TEXT,
        skills TEXT,
        image TEXT,
        code TEXT,
        date TEXT,
        tag TEXT,
        PRIMARY KEY(id)
        );
    """
)

# Delete all rows in portfolio table
cur.execute("DELETE FROM portfolio")
            
# Populate date from excel to database
projects_df.to_sql('portfolio', conn, if_exists='append', index=False)

# Close db
conn.close()
