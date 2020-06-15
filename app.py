from flask import Flask, render_template, url_for
app = Flask(__name__)

@app.route('/')
@app.route('/home')
def index():
    return render_template('/home.html')
    
@app.route('/blog')
def blog():
    return render_template('/blog.html')
app.run(debug=True)