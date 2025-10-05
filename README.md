
# File-Cloud 🐳

## Overview
**File-Cloud** is a lightweight, self-hosted cloud platform created using Flask. This project enables secure file management with user authentication, file upload, download, and deletion features. Now **fully containerized with Docker** for easy deployment anywhere! 

Originally designed to run on a spare laptop, it offers an efficient and private alternative to third-party cloud services. With Docker support, you can now deploy it locally, on cloud platforms (AWS, GCP, DigitalOcean), or anywhere Docker runs.

## Project Structure
```
├── pycache/ # Compiled Python files
├── app/ # Application logic (routes, templates, forms, etc.)
├── instance/ # Configuration and instance-specific data
├── migrations/ # Database migration files
├── uploads/ # User-uploaded files
├── README.md # Project documentation
├── init_db.py # Script to initialize the database
├── run.py # Main script to run the Flask application
```

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
  - Non-root Docker container execution.
- **🐳 Docker Support**: 
  - Fully containerized application
  - Multi-environment deployment (development/production)
  - Docker Hub integration for easy sharing
  - Docker Compose for orchestration
- **☁️ Cloud Ready**: Deploy on AWS, GCP, DigitalOcean, Heroku, or any cloud platform
- **Remote Access**: Access your cloud platform over the network using **ngrok** with HTTPS support.

## Prerequisites

### For Docker Deployment (Recommended)
- **Docker**: Version 20.10 or later
- **Docker Compose**: Version 2.0 or later
- **Operating System**: Windows, macOS, or Linux

### For Local Development
- **Operating System**: Linux Mint or any Linux-based OS, Windows, or macOS
- **Python**: Version 3.8 or higher
- **Tools**:
  - Flask
  - Flask-SQLAlchemy
  - Flask-WTF
  - SQLite
  - ngrok (optional)

## 🚀 Quick Start with Docker (Recommended)

### Option 1: Run from Docker Hub
```bash
# Pull and run the latest version
docker run -d -p 5000:5000 balakrishnas7/file-cloud:latest

# Or with data persistence
docker run -d -p 5000:5000 \
  -v file_uploads:/app/uploads \
  -v file_database:/app/instance \
  balakrishnas7/file-cloud:latest
```

### Option 2: Using Docker Compose
```bash
# Clone the repository
git clone https://github.com/BalaKrishnaS7/File-Cloud.git
cd File-Cloud

# Run with Docker Compose
docker-compose up -d

# Access at http://localhost:5000
```

### Option 3: Build Locally
```bash
# Clone and build
git clone https://github.com/BalaKrishnaS7/File-Cloud.git
cd File-Cloud
docker build -t file-cloud .
docker run -d -p 5000:5000 file-cloud
```

## 📋 Traditional Installation (Without Docker)
1. Clone the repository:
   ```bash
   git clone https://github.com/BalaKrishnaS7/File-Cloud.git
2. Navigate to the Project Directory:
   ```bash
   cd File-Cloud
3. Set up a virtual environment:
   ```bash
   python3 -m venv venv
   source venv/bin/activate  # On Linux/Mac
   # On Windows: venv\Scripts\activate
4. Install dependencies:
   ```bash
   pip install -r requirements.txt
5. Initialize the database:
   ```bash
   python init_db.py
6. Run the application:
    ```bash
    python run.py
7. Start ngrok to make the application accessible online (optional):
     ```bash
    ngrok http 5000

## Usage
### 🌐 Accessing the Application
1. **Local Docker**: http://localhost:5000
2. **Traditional setup**: http://127.0.0.1:5000  
3. **Using ngrok**: https://&lt;ngrok-generated-url&gt;
4. **Cloud deployment**: Your cloud provider's URL

### 👤 Getting Started
1. **Register**: Create a user account
2. **Log in**: Access your personal dashboard
3. **Manage files**:
   - **Upload**: Add files to your private directory
   - **Download**: Retrieve uploaded files
   - **Delete**: Remove unwanted files

## 🐳 Docker Hub
**Official Image**: `balakrishnas7/file-cloud:latest`
- **Repository**: https://hub.docker.com/r/balakrishnas7/file-cloud
- **Tags**: `latest`, `v1.0.0`

## Preview of website
 1.Home page
![home img](https://github.com/BalaKrishnaS7/File-Cloud/blob/main/home.png)


2. Dashboard page
![dashboard](https://github.com/BalaKrishnaS7/File-Cloud/blob/main/dashboard.png)
## ☁️ Cloud Deployment

### AWS EC2
```bash
docker pull balakrishnas7/file-cloud:latest
docker run -d -p 80:5000 balakrishnas7/file-cloud:latest
```

### Google Cloud Run
```bash
gcloud run deploy file-cloud \
  --image=balakrishnas7/file-cloud:latest \
  --port=5000 \
  --allow-unauthenticated
```

### DigitalOcean
```bash
docker pull balakrishnas7/file-cloud:latest
docker run -d -p 80:5000 balakrishnas7/file-cloud:latest
```

## 📚 Documentation
- **[Docker Deployment Guide](DOCKER_DEPLOYMENT.md)** - Comprehensive Docker setup
- **[Docker Hub Guide](DOCKER_HUB_GUIDE.md)** - Publishing and sharing
- **[Quick Deploy Guide](QUICK_DEPLOY.md)** - Fast deployment commands

## 🛠️ Development

### Docker Development
```bash
# Development with hot-reload
docker-compose up

# Production deployment
docker-compose -f docker-compose.prod.yml up -d

# With Nginx reverse proxy
docker-compose -f docker-compose.prod.yml --profile with-nginx up -d
```

### Local Development
```bash
# Install dependencies
pip install -r requirements.txt

# Run in development mode
python run.py
```

## Technologies Used
1. **Python**: Backend logic using Flask
2. **HTML/CSS**: Frontend for user interface  
3. **SQLite**: Lightweight database for user and file storage
4. **Docker**: Containerization and deployment
5. **Docker Compose**: Service orchestration
6. **Nginx**: Reverse proxy for production (optional)
7. **ngrok**: Remote access via secure tunnels

## 📁 Project Structure
```
File-Cloud/
├── 🐳 Docker Files
│   ├── Dockerfile                 # Main container definition
│   ├── docker-compose.yml         # Development setup
│   ├── docker-compose.prod.yml    # Production setup  
│   ├── docker-compose.hub.yml     # Docker Hub deployment
│   ├── .dockerignore              # Docker ignore rules
│   └── nginx.conf                 # Nginx configuration
├── 📋 Scripts
│   ├── deploy.sh                  # Linux deployment script
│   ├── deploy.bat                 # Windows deployment script
│   └── publish-to-dockerhub.bat   # Docker Hub publishing
├── 📖 Documentation  
│   ├── DOCKER_DEPLOYMENT.md       # Docker setup guide
│   ├── DOCKER_HUB_GUIDE.md        # Docker Hub guide
│   └── QUICK_DEPLOY.md            # Quick start guide
├── 🖥️ Application
│   ├── app/                       # Flask application
│   ├── run.py                     # Main application entry
│   ├── init_db.py                 # Database initialization
│   └── requirements.txt           # Python dependencies
└── 💾 Data
    ├── uploads/                   # User uploaded files
    └── instance/                  # Database and config
```

## License
This project is licensed under the MIT License.    


