# Docker Hub Publishing Guide for File-Cloud

This guide explains how to publish your File-Cloud Docker image to Docker Hub and deploy it from there.

## Prerequisites

- Docker Desktop installed and running
- Docker Hub account (free at [hub.docker.com](https://hub.docker.com))
- Your File-Cloud project with Dockerfile

## Step-by-Step Publishing Process

### 1. Create Docker Hub Repository (Optional)

1. Go to [Docker Hub](https://hub.docker.com)
2. Sign in to your account
3. Click "Create Repository"
4. Repository name: `file-cloud`
5. Description: "Self-hosted cloud storage platform built with Flask"
6. Visibility: Public (or Private if you prefer)
7. Click "Create"

### 2. Build Your Docker Image

```powershell
# Navigate to your project directory
cd "d:\projects\New folder\File-Cloud"

# Build the image locally
docker build -t file-cloud .

# Verify the image was created
docker images | findstr file-cloud
```

### 3. Login to Docker Hub

```powershell
# Login (you'll be prompted for username and password)
docker login

# Alternative: Login with token (more secure)
# docker login -u YOUR_USERNAME --password-stdin
```

### 4. Tag Your Image

Replace `YOUR_DOCKERHUB_USERNAME` with your actual Docker Hub username:

```powershell
# Tag with latest
docker tag file-cloud YOUR_DOCKERHUB_USERNAME/file-cloud:latest

# Tag with specific version (recommended for production)
docker tag file-cloud YOUR_DOCKERHUB_USERNAME/file-cloud:v1.0.0

# You can also tag with additional labels
docker tag file-cloud YOUR_DOCKERHUB_USERNAME/file-cloud:stable
```

### 5. Push to Docker Hub

```powershell
# Push all tags
docker push YOUR_DOCKERHUB_USERNAME/file-cloud:latest
docker push YOUR_DOCKERHUB_USERNAME/file-cloud:v1.0.0

# Or push all tags at once
docker push YOUR_DOCKERHUB_USERNAME/file-cloud --all-tags
```

### 6. Verify Upload

1. Go to your Docker Hub repository page
2. You should see your image with the tags you pushed
3. Note the pull command: `docker pull YOUR_DOCKERHUB_USERNAME/file-cloud`

## Using Your Published Image

### Quick Run Command

```powershell
# Run directly from Docker Hub
docker run -d -p 5000:5000 -v file_uploads:/app/uploads -v file_db:/app/instance YOUR_DOCKERHUB_USERNAME/file-cloud:latest
```

### Docker Compose with Published Image

Create a `docker-compose.hub.yml` file:

```yaml
version: '3.8'

services:
  file-cloud:
    image: YOUR_DOCKERHUB_USERNAME/file-cloud:latest
    container_name: file-cloud-hub
    ports:
      - "5000:5000"
    volumes:
      - file_uploads:/app/uploads
      - file_db:/app/instance
    environment:
      - FLASK_ENV=production
      - FLASK_DEBUG=0
    restart: unless-stopped

volumes:
  file_uploads:
  file_db:
```

Then run:
```powershell
docker-compose -f docker-compose.hub.yml up -d
```

## Automated Building and Pushing

### Create a Build Script

Create `build-and-push.bat`:

```batch
@echo off
set /p USERNAME="Enter your Docker Hub username: "
set /p VERSION="Enter version tag (e.g., v1.0.1): "

echo Building Docker image...
docker build -t file-cloud .

echo Tagging image...
docker tag file-cloud %USERNAME%/file-cloud:latest
docker tag file-cloud %USERNAME%/file-cloud:%VERSION%

echo Pushing to Docker Hub...
docker push %USERNAME%/file-cloud:latest
docker push %USERNAME%/file-cloud:%VERSION%

echo ✅ Successfully pushed to Docker Hub!
echo 📋 Pull command: docker pull %USERNAME%/file-cloud:latest
pause
```

### Using GitHub Actions (Optional)

Create `.github/workflows/docker-publish.yml`:

```yaml
name: Docker Build and Push

on:
  push:
    branches: [ main ]
    tags: [ 'v*' ]
  pull_request:
    branches: [ main ]

jobs:
  build-and-push:
    runs-on: ubuntu-latest
    steps:
    - uses: actions/checkout@v4
    
    - name: Set up Docker Buildx
      uses: docker/setup-buildx-action@v3
    
    - name: Login to Docker Hub
      uses: docker/login-action@v3
      with:
        username: ${{ secrets.DOCKERHUB_USERNAME }}
        password: ${{ secrets.DOCKERHUB_TOKEN }}
    
    - name: Extract metadata
      id: meta
      uses: docker/metadata-action@v5
      with:
        images: ${{ secrets.DOCKERHUB_USERNAME }}/file-cloud
    
    - name: Build and push
      uses: docker/build-push-action@v5
      with:
        context: .
        push: true
        tags: ${{ steps.meta.outputs.tags }}
        labels: ${{ steps.meta.outputs.labels }}
```

## Deployment Examples

### Local Deployment from Docker Hub

```powershell
# Pull and run
docker pull YOUR_DOCKERHUB_USERNAME/file-cloud:latest
docker run -d -p 5000:5000 YOUR_DOCKERHUB_USERNAME/file-cloud:latest
```

### Cloud Deployment Examples

#### AWS EC2
```bash
# On your EC2 instance
docker pull YOUR_DOCKERHUB_USERNAME/file-cloud:latest
docker run -d -p 80:5000 -v /opt/file-cloud/uploads:/app/uploads YOUR_DOCKERHUB_USERNAME/file-cloud:latest
```

#### Google Cloud Run
```bash
gcloud run deploy file-cloud \
  --image=YOUR_DOCKERHUB_USERNAME/file-cloud:latest \
  --port=5000 \
  --allow-unauthenticated
```

#### DigitalOcean
```bash
# On your droplet
docker pull YOUR_DOCKERHUB_USERNAME/file-cloud:latest
docker run -d -p 80:5000 YOUR_DOCKERHUB_USERNAME/file-cloud:latest
```

### Docker Swarm Deployment

```yaml
# docker-stack.yml
version: '3.8'

services:
  file-cloud:
    image: YOUR_DOCKERHUB_USERNAME/file-cloud:latest
    ports:
      - "80:5000"
    volumes:
      - uploads:/app/uploads
      - database:/app/instance
    deploy:
      replicas: 3
      restart_policy:
        condition: on-failure
    networks:
      - file-cloud-net

volumes:
  uploads:
  database:

networks:
  file-cloud-net:
    driver: overlay
```

Deploy with:
```bash
docker stack deploy -c docker-stack.yml file-cloud-stack
```

## Version Management Best Practices

### Semantic Versioning
- `v1.0.0` - Major version
- `v1.1.0` - Minor version (new features)
- `v1.1.1` - Patch version (bug fixes)

### Tagging Strategy
```powershell
# Always tag with version and latest
docker tag file-cloud YOUR_USERNAME/file-cloud:v1.2.0
docker tag file-cloud YOUR_USERNAME/file-cloud:latest

# Optional: Environment-specific tags
docker tag file-cloud YOUR_USERNAME/file-cloud:production
docker tag file-cloud YOUR_USERNAME/file-cloud:stable
```

## Troubleshooting

### Common Issues

1. **Authentication failed**
   ```powershell
   docker logout
   docker login
   ```

2. **Image not found**
   - Check if the repository name is correct
   - Ensure the image was pushed successfully

3. **Permission denied**
   - Make sure you're logged in to the correct account
   - Check if the repository exists and you have write access

### Security Best Practices

1. **Use Docker Hub tokens instead of passwords**
   ```powershell
   docker login -u YOUR_USERNAME --password-stdin
   ```

2. **Don't include sensitive data in images**
   - Use environment variables for secrets
   - Use Docker secrets in production

3. **Scan images for vulnerabilities**
   ```powershell
   docker scan YOUR_USERNAME/file-cloud:latest
   ```

## Monitoring Your Docker Hub Repository

- **Pull statistics**: View download counts
- **Webhooks**: Set up notifications for pushes
- **Automated builds**: Connect to GitHub for automatic builds

---

🎉 **Congratulations!** Your File-Cloud application is now available on Docker Hub and can be deployed anywhere Docker runs!