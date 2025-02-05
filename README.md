
# File-Cloud

## Overview
**File-Cloud** is a lightweight, self-hosted cloud platform created using Flask. This project enables secure file management with user authentication, file upload, download, and deletion features. Designed to run on a spare laptop, it offers an efficient and private alternative to third-party cloud services, with remote access made possible using **ngrok**.

## Project Structure
├── pycache/ # Compiled Python files ├── app/ # Application logic (routes, templates, forms, etc.) ├── instance/ # Configuration and instance-specific data ├── migrations/ # Database migration files ├── uploads/ # User-uploaded files ├── README.md # Project documentation ├── init_db.py # Script to initialize the database ├── run.py # Main script to run the Flask application

markdown
Copy code

## Features
- **User Authentication**: Secure registration, login, and logout with hashed passwords.
- **File Management**: 
  - Upload files to user-specific directories.
  - View, download, and delete files securely.
- **Database**: SQLite database for user management and file metadata.
- **Security**:
  - Password hashing for secure credential storage.
  - CSRF protection for all forms using Flask-WTF.
- **Remote Access**: Access your cloud platform over the network using **ngrok** with HTTPS support.

## Prerequisites
- **Operating System**: Linux Mint or any Linux-based OS.
- **Python**: Version 3.8 or higher.
- **Tools**:
  - Flask
  - Flask-SQLAlchemy
  - Flask-WTF
  - SQLite
  - ngrok

## Installation
1. Clone the repository:
   ```bash
   git clone https://github.com/BalaKrishnaS7/file-cloud.git
2. Navigate to the Project Directory:
   ```bash
   cd file-cloud
3. Set up a virtual environment:
   ```bash
   python3 -m venv venv
   source venv/bin/activate  # On Linux/Mac
4. Install dependencies:
   Run the following commands to install required dependencies:
   ```bash
   pip install flask
   pip install flask-wtf
   pip install flask-sqlalchemy
5. Initialize the database:
   ```bash
   python init_db.py
6. Run the application:
    ```bash
    python run.py
7. Start ngrok to make the application accessible online:
    ```bash
    ngrok http 5000

## Usage
  1. Access the application locally:
     ```bash
     http://127.0.0.1:5000
  1. using ngrok:
      ````bash
      https://<ngrok-generated-url>
  2. Register: Create a user account.
  3. Log in: Access your dashboard.
  4. Manage files:
      1. Upload: Add files to your private directory.
      2. Download: Retrieve uploaded files.
      3. Delete: Remove unwanted files.

[home img](https://github.com/BalaKrishnaS7/File-Cloud/blob/main/home.png)
## Technologies Used
  1. Python: Backend logic using Flask.
  2. HTML/CSS: Frontend for user interface.
  3. SQLite: Lightweight database for user and file storage.
  4. ngrok: Remote access via secure tunnels.

 ## License
   This project is licensed under the MIT License.    


