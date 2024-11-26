from flask import Flask
from flask_sqlalchemy import SQLAlchemy
import os

# Initialize Flask app
app = Flask(__name__)

# Print the current working directory
print("Current working directory:", os.getcwd())

# Secret Key for CSRF protection
app.config['SECRET_KEY'] = os.urandom(24)

# Database Configuration
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///cloud.db'
db = SQLAlchemy(app)

# File Upload Configuration
app.config['UPLOAD_FOLDER'] = os.path.join(os.getcwd(), 'uploads')

# Ensure the uploads folder exists
os.makedirs(app.config['UPLOAD_FOLDER'], exist_ok=True)

# Import routes (ensure this is after app creation)
from app import routes

