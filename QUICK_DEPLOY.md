# 🚀 File-Cloud Docker Hub Deployment

Your File-Cloud image is now live on Docker Hub! 🎉

**Docker Hub Repository**: https://hub.docker.com/r/balakrishnas7/file-cloud

## ⚡ Quick Deployment Options

### 1. Simple Run Command
```powershell
# Run directly from Docker Hub
docker run -d -p 5000:5000 balakrishnas7/file-cloud:v1.0.0

# Access at: http://localhost:5000
```

### 2. With Data Persistence
```powershell
# Run with persistent storage for uploads and database
docker run -d -p 5000:5000 ^
  -v file_uploads:/app/uploads ^
  -v file_database:/app/instance ^
  --name file-cloud-app ^
  balakrishnas7/file-cloud:v1.0.0
```

### 3. Using Docker Compose (Recommended)
```powershell
# Use the provided docker-compose.hub.yml
docker-compose -f docker-compose.hub.yml up -d

# Access at: http://localhost:5000
```

### 4. Production Deployment
```powershell
# For production (port 80)
docker run -d -p 80:5000 ^
  -v file_uploads:/app/uploads ^
  -v file_database:/app/instance ^
  -e FLASK_ENV=production ^
  --restart unless-stopped ^
  --name file-cloud-prod ^
  balakrishnas7/file-cloud:v1.0.0

# Access at: http://localhost
```

## 🌍 Cloud Deployment Examples

### AWS EC2
```bash
# On your EC2 instance
docker pull balakrishnas7/file-cloud:v1.0.0
docker run -d -p 80:5000 -v /opt/uploads:/app/uploads balakrishnas7/file-cloud:v1.0.0
```

### Google Cloud Run
```bash
gcloud run deploy file-cloud \
  --image=balakrishnas7/file-cloud:v1.0.0 \
  --port=5000 \
  --allow-unauthenticated
```

### DigitalOcean Droplet
```bash
docker pull balakrishnas7/file-cloud:v1.0.0
docker run -d -p 80:5000 balakrishnas7/file-cloud:v1.0.0
```

## 📊 Management Commands

```powershell
# View running containers
docker ps

# View logs
docker logs file-cloud-app

# Stop container
docker stop file-cloud-app

# Remove container
docker rm file-cloud-app

# Update to latest version
docker pull balakrishnas7/file-cloud:latest
docker stop file-cloud-app
docker rm file-cloud-app
docker run -d -p 5000:5000 balakrishnas7/file-cloud:latest
```

## 🔄 Available Tags

- `balakrishnas7/file-cloud:v1.0.0` - Your current version
- `balakrishnas7/file-cloud:latest` - Latest version (if pushed)

## ✅ You're All Set!

Your File-Cloud application is now:
- ✅ Published on Docker Hub
- ✅ Ready for deployment anywhere
- ✅ Easy to share with others
- ✅ Cloud deployment ready

**Share your work**: Others can now run your app with just:
```powershell
docker run -p 5000:5000 balakrishnas7/file-cloud:v1.0.0
```