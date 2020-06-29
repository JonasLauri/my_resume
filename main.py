from app import app, db
import models
import views

# Blueprints connection
from entries.blueprint import entries
app.register_blueprint(entries, url_prefix='/posts')

# Run directly
if __name__ == '__main__':
    app.run(debug=True)
