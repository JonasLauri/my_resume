from flask import Flask, render_template, url_for, flash, redirect
from flask_sqlalchemy import SQLAlchemy
from forms import RegistrationForm, LoginForm

# App and db inits, configs
app = Flask(__name__)
app.config['SECRET_KEY'] = '91f3cd4f5c6b411e7c60794b3d9d31af'
app.config['DATABASE_URI'] = 'sqlite:///site.db'
DATABASE = 'site.db'
db = SQLAlchemy(app)

# Specify user table
class User(db.Model):
    id 


# Website's routes
@app.route('/')
@app.route('/home')
def index():
    return render_template('/home.html')

@app.route('/about')
def about():
    return render_template('/about.html')

@app.route('/blog')
def blog():
    return render_template('/blog.html')

@app.route('/register', methods=['GET', 'POST'])
def register():
    form = RegistrationForm()
    if form.validate_on_submit():
        flash(f'Account created for {form.username.data}!',  'primary')
        return redirect(url_for('index'))
    return render_template('/includes/_register.html', title='Register', form=form)

@app.route('/login', methods=['GET', 'POST'])
def login():
    form = LoginForm()
    if form.validate_on_submit():
        if form.email.data == "jonasllaurinai@gmail.com":
            flash(f'You have been logged in!', 'primary')
            return redirect(url_for('index'))
        else:
            flash('Login unsuccessful. Please check username and password', 'danger')
    return render_template('/includes/_login.html', title='Login', form=form)


# Run directly
if __name__ == '__main__':
    app.run(debug=True)
