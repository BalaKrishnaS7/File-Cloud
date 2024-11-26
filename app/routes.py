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
    return "Welcome to Your Cloud"

@app.route('/register', methods=['GET', 'POST'])
def register():
    form = RegisterForm()
    if form.validate_on_submit():  # Validates CSRF and form data
        username = form.username.data
        password = form.password.data
        hashed_password = generate_password_hash(password, method='pbkdf2:sha256')

        # Check if the username already exists
        if User.query.filter_by(username=username).first():
            flash('Username already exists!', 'danger')
            return redirect(url_for('register'))

        # Add the new user to the database
        new_user = User(username=username, password=hashed_password)
        db.session.add(new_user)
        db.session.commit()
        flash('Registration successful! You can now log in.', 'success')
        return redirect(url_for('login'))

    return render_template('register.html', form=form)

@app.route('/login', methods=['GET', 'POST'])
def login():
    form = LoginForm()
    if form.validate_on_submit():
        username = form.username.data
        password = form.password.data
        user = User.query.filter_by(username=username).first()
        if user and check_password_hash(user.password, password):
            session['user_id'] = user.id
            flash('Login successful!', 'success')
            return redirect(url_for('dashboard'))
        flash('Invalid credentials!', 'danger')
    return render_template('login.html', form=form)

@app.route('/logout')
def logout():
    session.pop('user_id', None)
    flash('Logged out successfully!', 'success')
    return redirect(url_for('login'))

@app.route('/dashboard')
def dashboard():
    if 'user_id' not in session:
        flash('Please log in to continue.', 'danger')
        return redirect(url_for('login'))

    user_id = session['user_id']
    files = File.query.filter_by(user_id=user_id).all()
    return render_template('dashboard.html', files=files)

@app.route('/upload', methods=['GET', 'POST'])
def upload_file():
    if 'user_id' not in session:
        flash('Please log in to continue.', 'danger')
        return redirect(url_for('login'))

    form = UploadForm()
    if form.validate_on_submit():
        file = form.file.data
        if file and allowed_file(file.filename):
            filename = secure_filename(file.filename)
            timestamp = datetime.now().strftime('%Y%m%d%H%M%S')
            unique_filename = f"{timestamp}_{filename}"
            filepath = os.path.join(app.config['UPLOAD_FOLDER'], unique_filename)
            file.save(filepath)

            new_file = File(filename=unique_filename, filepath=filepath, user_id=session['user_id'])
            db.session.add(new_file)
            db.session.commit()
            flash('File uploaded successfully!', 'success')
            return redirect(url_for('dashboard'))
        flash('Invalid file type!', 'danger')
    return render_template('upload.html', form=form)


@app.route('/delete/<int:file_id>', methods=['POST'])
def delete_file(file_id):
    if 'user_id' not in session:
        flash('Please log in to continue.', 'danger')
        return redirect(url_for('login'))

    file = File.query.get(file_id)
    if file and file.user_id == session['user_id']:
        os.remove(file.filepath)  # Delete file from the filesystem
        db.session.delete(file)  # Remove it from the database
        db.session.commit()
        flash('File deleted successfully!', 'success')
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
        # Use only the filename with send_from_directory
        return send_from_directory(app.config['UPLOAD_FOLDER'], file.filename)
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
        return send_from_directory(app.config['UPLOAD_FOLDER'], file.filename, as_attachment=True)
    else:
        flash('File not found or unauthorized!', 'danger')
        return redirect(url_for('dashboard'))




@app.route('/test-static')
def test_static():
    test_filename = 'example.txt'  # Replace with the name of an existing file in your uploads folder
    test_path = os.path.join(app.config['UPLOAD_FOLDER'], test_filename)
    
    print("Test static file path:", test_path)

    if not os.path.exists(test_path):
        return "File does not exist at the expected location!", 404

    return send_from_directory(app.config['UPLOAD_FOLDER'], test_filename)

