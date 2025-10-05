# Docker Deployment Guide for File-Cloud

This guide provides instructions for containerizing and deploying the File-Cloud application using Docker for both local development and cloud/production environments.

## Prerequisites

- Docker Engine 20.10 or later
- Docker Compose v2.0 or later
- Git (for cloning the repository)

## Project Structure

After adding Docker support, your project structure will include:

```
File-Cloud/
├── Dockerfile                 # Main Docker image definition
├── docker-compose.yml         # Local development setup
├── docker-compose.prod.yml    # Production deployment setup
├── .dockerignore             # Files to exclude from Docker context
├── requirements.txt          # Python dependencies
├── nginx.conf               # Nginx configuration for production
└── ... (rest of your existing files)
```

## Local Development Deployment

### Quick Start

1. **Clone the repository** (if not already done):
   ```bash
   git clone https://github.com/BalaKrishnaS7/File-Cloud.git
   cd File-Cloud
   ```

2. **Build and run with Docker Compose**:
   ```bash
   docker-compose up --build
   ```

3. **Access the application**:
   - Open your browser and navigate to `http://localhost:5000`
   - The application will be running in development mode with hot-reload enabled

### Development Commands

- **Start services in background**:
  ```bash
  docker-compose up -d
  ```

- **View logs**:
  ```bash
  docker-compose logs -f
  ```

- **Stop services**:
  ```bash
  docker-compose down
  ```

- **Rebuild after code changes**:
  ```bash
  docker-compose up --build
  ```

- **Access container shell**:
  ```bash
  docker-compose exec file-cloud bash
  ```

### Development Features

- **Volume mounting**: Your local code is mounted into the container for live updates
- **Database persistence**: SQLite database persists in `./instance` directory
- **File uploads**: Uploaded files persist in `./uploads` directory
- **Debug mode**: Flask runs with debug=True for development

## Production/Cloud Deployment

### Option 1: Simple Production Deployment

1. **Use the production compose file**:
   ```bash
   docker-compose -f docker-compose.prod.yml up -d --build
   ```

2. **Access the application**:
   - The app will be available on port 80: `http://your-server-ip`

### Option 2: Production with Nginx Reverse Proxy

1. **Deploy with Nginx**:
   ```bash
   docker-compose -f docker-compose.prod.yml --profile with-nginx up -d --build
   ```

2. **Configure SSL** (optional):
   - Place your SSL certificates in a `ssl/` directory:
     ```
     ssl/
     ├── cert.pem
     └── key.pem
     ```
   - Uncomment the HTTPS server section in `nginx.conf`
   - Update the server_name in `nginx.conf` with your domain

### Cloud Platform Specific Deployments

#### AWS EC2

1. **Launch an EC2 instance** with Docker installed
2. **Clone your repository**:
   ```bash
   git clone https://github.com/BalaKrishnaS7/File-Cloud.git
   cd File-Cloud
   ```
3. **Deploy**:
   ```bash
   docker-compose -f docker-compose.prod.yml up -d --build
   ```
4. **Configure security groups** to allow traffic on ports 80/443

#### Google Cloud Platform (Cloud Run)

1. **Build and push to Google Container Registry**:
   ```bash
   # Set your project ID
   export PROJECT_ID=your-gcp-project-id
   
   # Build and tag the image
   docker build -t gcr.io/$PROJECT_ID/file-cloud .
   
   # Push to GCR
   docker push gcr.io/$PROJECT_ID/file-cloud
   ```

2. **Deploy to Cloud Run**:
   ```bash
   gcloud run deploy file-cloud \
     --image gcr.io/$PROJECT_ID/file-cloud \
     --port 5000 \
     --allow-unauthenticated \
     --region us-central1
   ```

#### DigitalOcean Droplet

1. **Create a Droplet** with Docker pre-installed
2. **Deploy using Docker Compose**:
   ```bash
   git clone https://github.com/BalaKrishnaS7/File-Cloud.git
   cd File-Cloud
   docker-compose -f docker-compose.prod.yml up -d --build
   ```

#### Heroku (using Container Registry)

1. **Login to Heroku Container Registry**:
   ```bash
   heroku login
   heroku container:login
   ```

2. **Create a Heroku app**:
   ```bash
   heroku create your-file-cloud-app
   ```

3. **Build and push container**:
   ```bash
   heroku container:push web -a your-file-cloud-app
   heroku container:release web -a your-file-cloud-app
   ```

## Environment Variables

You can customize the deployment using environment variables:

| Variable | Description | Default |
|----------|-------------|---------|
| `FLASK_ENV` | Flask environment | `production` |
| `FLASK_DEBUG` | Enable debug mode | `0` |
| `SECRET_KEY` | Flask secret key | Auto-generated |

Example with custom environment:
```bash
docker run -e FLASK_ENV=production -e FLASK_DEBUG=0 -p 5000:5000 file-cloud
```

## Data Persistence

### Volumes

The Docker setup uses volumes to persist important data:

- **Database**: SQLite database stored in `/app/instance`
- **Uploads**: User uploaded files stored in `/app/uploads`

### Backup Strategy

1. **Backup database**:
   ```bash
   docker cp file-cloud-app:/app/instance/cloud.db ./backup/
   ```

2. **Backup uploads**:
   ```bash
   docker cp file-cloud-app:/app/uploads ./backup/
   ```

3. **Automated backups**: Set up cron jobs or use cloud storage solutions

## Security Considerations

### Production Security

1. **Use HTTPS**: Configure SSL certificates with Nginx
2. **Firewall**: Only expose necessary ports (80, 443)
3. **Updates**: Regularly update base images and dependencies
4. **Secrets**: Use Docker secrets or environment files for sensitive data
5. **Non-root user**: The container runs as a non-root user
6. **Read-only filesystem**: Production container uses read-only root filesystem

### Environment Files

Create a `.env` file for sensitive configuration:
```bash
# .env
SECRET_KEY=your-super-secret-key-here
FLASK_ENV=production
```

Use with Docker Compose:
```bash
docker-compose --env-file .env -f docker-compose.prod.yml up -d
```

## Monitoring and Logging

### Health Checks

The Docker containers include health checks that:
- Monitor application availability
- Restart containers if unhealthy
- Integrate with orchestration platforms

### Logging

- **Development**: Logs appear in console
- **Production**: Logs are captured by Docker logging driver
- **Log rotation**: Configured to prevent disk space issues

View logs:
```bash
# All services
docker-compose logs -f

# Specific service
docker-compose logs -f file-cloud

# Production
docker-compose -f docker-compose.prod.yml logs -f
```

## Troubleshooting

### Common Issues

1. **Port already in use**:
   ```bash
   # Change port in docker-compose.yml
   ports:
     - "5001:5000"  # Use different host port
   ```

2. **Permission issues**:
   ```bash
   # Fix file permissions
   sudo chown -R $USER:$USER uploads/ instance/
   ```

3. **Database initialization**:
   ```bash
   # Reinitialize database
   docker-compose exec file-cloud python init_db.py
   ```

4. **Container won't start**:
   ```bash
   # Check logs
   docker-compose logs file-cloud
   
   # Debug with shell
   docker-compose run --rm file-cloud bash
   ```

### Performance Tuning

1. **Resource limits**: Add resource limits to docker-compose.yml
2. **Multi-stage builds**: Optimize Dockerfile for smaller images
3. **Caching**: Use Redis for session storage in high-traffic deployments

## Scaling

For high-traffic deployments:

1. **Horizontal scaling**:
   ```bash
   docker-compose -f docker-compose.prod.yml up -d --scale file-cloud=3
   ```

2. **Load balancer**: Configure Nginx for load balancing
3. **External database**: Use PostgreSQL or MySQL instead of SQLite
4. **Container orchestration**: Consider Kubernetes for complex deployments

## Support

- **Issues**: Report issues on GitHub
- **Documentation**: Check the main README.md for application-specific details
- **Docker Hub**: Consider publishing images to Docker Hub for easier deployment

---

This containerized setup provides a robust, scalable, and secure way to deploy your File-Cloud application in any environment!