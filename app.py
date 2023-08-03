# Importing required modules
import os
import hashlib
from datetime import datetime
from flask import Flask, render_template, request, redirect

from flask_sqlalchemy import SQLAlchemy

# Creating the Flask app
app = Flask(__name__)

# Creating ShortURL
def shorten_url(url):
    hash = hashlib.sha1(url.encode('utf-8')).hexdigest()[:6]
    return hash

# Creating SQLite Database
app.config['SQLALCHEMY_DATABASE_URI'] = "sqlite:///url.db"
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
db = SQLAlchemy(app)

class ShortUrls(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    original_url = db.Column(db.String(500), nullable=False)
    short_id = db.Column(db.String(20), nullable=False, unique=True)
    created_at = db.Column(db.DateTime(), default=datetime.now(), nullable=False)

    def __init__(self, original_url, short_id):
        self.original_url = original_url
        self.short_id = short_id

    def get_short_url(self):
        return f'/{self.short_id}'

with app.app_context():
    db.create_all()

# Defining the index route
@app.route('/', methods=['POST', 'GET'])
def index():
    short_url = None
    if request.method == 'POST':
        url_received = request.form['url']
        short_url_id = shorten_url(url_received)
        short_url = ShortUrls(original_url=url_received, short_id=short_url_id)
        db.session.add(short_url)
        db.session.commit()
        short_url = request.url_root + short_url.get_short_url()
    return render_template('index.html', short_url=short_url)

# Route for redirection
@app.route('/<short_id>')
def redirect_to_url(short_id):
    short_url = ShortUrls.query.filter_by(short_id=short_id).first_or_404()
    return redirect(short_url.original_url)

# Running the Flask application
if __name__ == '__main__':
    app.run(debug=True)
