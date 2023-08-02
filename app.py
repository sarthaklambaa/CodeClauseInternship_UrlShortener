# Importing required modules
import os
import hashlib
from datetime import datetime
from flask import Flask, render_template, request
from flask_sqlalchemy import SQLAlchemy
# Creating the Flask app
app = Flask(__name__)

# Creating ShortURL
def shorten_url(url):
    hash = hashlib.sha1(url.encode('utf-8')).hexdigest()[:6]
    return hash

# Creating SQLite Database
app.config['SQLALCHEMY_DATABASE_URI'] = "sqlite:///url.db"
app.config['SQLALCHEMY_DATABASE_URI'] = "sqlite:///url.db" #url is name
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
db = SQLAlchemy(app)

class ShortUrls(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    original_url = db.Column(db.String(500), nullable=False)
    short_id = db.Column(db.String(20), nullable=False, unique=True)
    created_at = db.Column(db.DateTime(), default=datetime.now(), nullable=False)

    def __init__(self, long, short):
      self.long = long
      self.short = short

with app.app_context():
    db.create_all()

# Defining the index route
@app.route('/', methods = ['POST','GET'])
def index():
   if request.method == 'POST':
      url_received = request.form['url']
      short_url = shorten_url(url_received)
      print(short_url)
      return short_url
   else:
      return render_template('index.html')

# Running the Flask application
if __name__ == '__main__':
   app.run(debug=True)