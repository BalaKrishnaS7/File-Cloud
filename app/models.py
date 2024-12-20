from app import db
from datetime import datetime

# User model
class User(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(50), unique=True, nullable=False)
    password = db.Column(db.String(100), nullable=False)
    # Relationship to associate files with the user
    files = db.relationship('File', backref='owner', lazy=True)

    def __repr__(self):
        return f"<User {self.username}>"

# File model
class File(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    filename = db.Column(db.String(100), nullable=False)  # Name of the uploaded file
    filepath = db.Column(db.String(300), nullable=False)  # Full path to the file (including user folder)
    upload_date = db.Column(db.DateTime, default=datetime.utcnow)  # Timestamp for the upload
    user_id = db.Column(db.Integer, db.ForeignKey('user.id'), nullable=False)  # Link to the user who owns the file

    def __repr__(self):
        return f"<File {self.filename} belonging to User {self.user_id}>"

