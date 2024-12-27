
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
