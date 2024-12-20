from flask import Flask
from flask_sqlalchemy import SQLAlchemy
from flask_migrate import Migrate  # Import Flask-Migrate for database migrations
import os

# Initialize Flask app
app = Flask(__name__)

# Print the current working directory for debugging
print("Current working directory:", os.getcwd())

# Secret Key for CSRF protection
app.config['SECRET_KEY'] = os.urandom(24)

# Database Configuration
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///cloud.db'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False  # Disable track modifications for performance
db = SQLAlchemy(app)

# Initialize Flask-Migrate
migrate = Migrate(app, db)

# File Upload Configuration
app.config['UPLOAD_FOLDER'] = os.path.join(os.getcwd(), 'uploads')

# Ensure the uploads folder exists
os.makedirs(app.config['UPLOAD_FOLDER'], exist_ok=True)
print("Uploads folder ensured at:", app.config['UPLOAD_FOLDER'])  # Debugging output

# Import routes after app, db, and migrations are initialized
from app import routes

