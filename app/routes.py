from flask import render_template, redirect, url_for, request, flash, session, send_from_directory, Response
from app import app, db
from app.models import User, File
from werkzeug.security import generate_password_hash, check_password_hash
from werkzeug.utils import secure_filename
from flask_wtf.csrf import CSRFProtect
from datetime import datetime
from app.forms import LoginForm, UploadForm, RegisterForm
import os

# CSRF Protection
csrf = CSRFProtect(app)
app.config['SECRET_KEY'] = 'e7a6340ff4d82791fe8050993b712c9450dab5fb59c33a23'

UPLOAD_FOLDER = os.path.join(os.getcwd(), 'uploads')
app.config['UPLOAD_FOLDER'] = UPLOAD_FOLDER
os.makedirs(app.config['UPLOAD_FOLDER'], exist_ok=True)
ALLOWED_EXTENSIONS = {'txt', 'pdf', 'png', 'jpg', 'jpeg', 'gif', 'mp4', 'mkv'}

# Helper function to check allowed file types
def allowed_file(filename):
    return '.' in filename and filename.rsplit('.', 1)[1].lower() in ALLOWED_EXTENSIONS

@app.route('/')
def home():
    return render_template('home.html')  # Render the landing page template

# register route
@app.route('/register', methods=['GET', 'POST'])
def register():
    form = RegisterForm()
    if form.validate_on_submit():
        username = form.username.data
        password = form.password.data
        hashed_password = generate_password_hash(password, method='pbkdf2:sha256')

        # Check if the user already exists
        if User.query.filter_by(username=username).first():
            flash('Username already exists!', 'danger')  # Flash error message
            return redirect(url_for('register'))  # Redirect to registration page if username exists

        # Create a new user and save to the database
        new_user = User(username=username, password=hashed_password)
        db.session.add(new_user)
        db.session.commit()

        # Create a folder for the user in the uploads directory
        user_folder = os.path.join(app.config['UPLOAD_FOLDER'], username)
        os.makedirs(user_folder, exist_ok=True)  # Ensure the folder is created

        flash('Registration successful! You can now log in.', 'success')  # Flash success message
        return redirect(url_for('login'))  # Redirect to the login page after successful registration
    else:
        # Print validation errors if the form is not valid
        print(form.errors)

    return render_template('register.html', form=form)


# login route
@app.route('/login', methods=['GET', 'POST'])
def login():
    form = LoginForm()
    if form.validate_on_submit():
        username = form.username.data
        password = form.password.data

        # Check if the user exists
        user = User.query.filter_by(username=username).first()
        if user and check_password_hash(user.password, password):  # Validate the password
            session['user_id'] = user.id  # Store user ID in session
            flash('Login successful!', 'success')  # Flash a success message
            return redirect(url_for('dashboard'))  # Redirect to dashboard
        else:
            flash('Invalid username or password', 'danger')  # Show error message for invalid login

    return render_template('login.html', form=form)


@app.route('/logout')
def logout():
    session.pop('user_id', None)
    flash('Logged out successfully!', 'success')
    return redirect(url_for('login'))

# Upload file route
@app.route('/upload', methods=['GET', 'POST'])
def upload_file():
    if 'user_id' not in session:
        flash('Please log in to continue.', 'danger')
        return redirect(url_for('login'))

    form = UploadForm()
    if form.validate_on_submit():
        file = form.file.data  # Get the file from the form
        if file:
            # Get the logged-in user's folder
            user = User.query.get(session['user_id'])
            user_folder = os.path.join(app.config['UPLOAD_FOLDER'], user.username)

            # Ensure the folder exists
            os.makedirs(user_folder, exist_ok=True)

            # Save the file in the user's folder
            filename = file.filename
            filepath = os.path.join(user_folder, filename)
            file.save(filepath)

            # Save file details to the database
            new_file = File(filename=filename, filepath=filepath, user_id=user.id)
            db.session.add(new_file)
            db.session.commit()

            flash('File uploaded successfully!', 'success')
            return redirect(url_for('dashboard'))  # Redirect to the dashboard after upload
    return render_template('upload.html', form=form)

# Dashboard route
@app.route('/dashboard')
def dashboard():
    if 'user_id' not in session:
        flash('Please log in to continue.', 'danger')
        return redirect(url_for('login'))

    # Fetch files uploaded by the user
    user_id = session['user_id']
    files = File.query.filter_by(user_id=user_id).all()
    return render_template('dashboard.html', files=files)


@app.route('/delete/<int:file_id>', methods=['POST'])
def delete_file(file_id):
    if 'user_id' not in session:
        flash('Please log in to continue.', 'danger')
        return redirect(url_for('login'))

    # Fetch the file record from the database
    file = File.query.get(file_id)
    if file and file.user_id == session['user_id']:
        # Get the user's folder
        user = User.query.get(session['user_id'])
        user_folder = os.path.join(app.config['UPLOAD_FOLDER'], user.username)
        file_path = os.path.join(user_folder, file.filename)

        # Check if the file exists
        if os.path.exists(file_path):
            # Delete the file from the filesystem
            os.remove(file_path)
            print(f"Deleted file: {file_path}")  # Debugging

            # Remove the file record from the database
            db.session.delete(file)
            db.session.commit()
            flash('File deleted successfully!', 'success')
        else:
            print(f"File not found for deletion: {file_path}")  # Debugging
            flash('File not found on the server!', 'danger')
    else:
        flash('File not found or unauthorized!', 'danger')

    return redirect(url_for('dashboard'))


@app.route('/view/<int:file_id>')
def view_file(file_id):
    if 'user_id' not in session:
        flash('Please log in to continue.', 'danger')
        return redirect(url_for('login'))

    file = File.query.get(file_id)
    if file and file.user_id == session['user_id']:
        user = User.query.get(session['user_id'])
        user_folder = os.path.join(app.config['UPLOAD_FOLDER'], user.username)
        file_path = os.path.join(user_folder, file.filename)

        if not os.path.exists(file_path):
            flash('File not found!', 'danger')
            return redirect(url_for('dashboard'))

        return send_from_directory(user_folder, file.filename)
    else:
        flash('File not found or unauthorized!', 'danger')
        return redirect(url_for('dashboard'))


@app.route('/download/<int:file_id>')
def download_file(file_id):
    if 'user_id' not in session:
        flash('Please log in to continue.', 'danger')
        return redirect(url_for('login'))

    file = File.query.get(file_id)
    if file and file.user_id == session['user_id']:
        user = User.query.get(session['user_id'])
        user_folder = os.path.join(app.config['UPLOAD_FOLDER'], user.username)
        file_path = os.path.join(user_folder, file.filename)

        if not os.path.exists(file_path):
            flash('File not found!', 'danger')
            return redirect(url_for('dashboard'))

        return send_from_directory(user_folder, file.filename, as_attachment=True)
    else:
        flash('File not found or unauthorized!', 'danger')
        return redirect(url_for('dashboard'))

