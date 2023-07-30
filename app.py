# Importing required modules
import os
from datetime import datetime
from flask import Flask, render_template
from flask_sqlalchemy import SQLAlchemy

# Creating the Flask app
app = Flask(__name__)

# Creating SQLite Database
app.config['SQLALCHEMY_DATABASE_URI'] = "sqlite:///url.db"
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
db = SQLAlchemy(app)

# Defining the ShortUrls DB Schema  
class ShortUrls(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    original_url = db.Column(db.String(500), nullable=False)
    short_id = db.Column(db.String(20), nullable=False, unique=True)
    created_at = db.Column(db.DateTime(), default=datetime.now(), nullable=False)

# Defining the index route
@app.route('/')
def index():
   return render_template('index.html')

# Running the Flask application
if __name__ == '__main__':
   app.run(debug=True)