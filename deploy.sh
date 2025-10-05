#!/bin/bash

# File-Cloud Docker Deployment Script
# This script helps you deploy File-Cloud with Docker quickly

set -e

echo "🐳 File-Cloud Docker Deployment Script"
echo "======================================"

# Function to check if Docker is installed
check_docker() {
    if ! command -v docker &> /dev/null; then
        echo "❌ Docker is not installed. Please install Docker first."
        echo "Visit: https://docs.docker.com/get-docker/"
        exit 1
    fi
    
    if ! command -v docker-compose &> /dev/null && ! docker compose version &> /dev/null; then
        echo "❌ Docker Compose is not installed. Please install Docker Compose first."
        echo "Visit: https://docs.docker.com/compose/install/"
        exit 1
    fi
    
    echo "✅ Docker and Docker Compose are installed"
}

# Function to create necessary directories
create_directories() {
    echo "📁 Creating necessary directories..."
    mkdir -p uploads instance ssl
    echo "✅ Directories created"
}

# Function for local development deployment
deploy_local() {
    echo "🚀 Starting local development deployment..."
    create_directories
    
    if docker-compose up --build -d; then
        echo "✅ File-Cloud is running in development mode!"
        echo "🌐 Access your application at: http://localhost:5000"
        echo "📋 To view logs: docker-compose logs -f"
        echo "🛑 To stop: docker-compose down"
    else
        echo "❌ Failed to start local deployment"
        exit 1
    fi
}

# Function for production deployment
deploy_production() {
    echo "🚀 Starting production deployment..."
    create_directories
    
    read -p "Do you want to include Nginx reverse proxy? (y/N): " include_nginx
    
    if [[ $include_nginx =~ ^[Yy]$ ]]; then
        if docker-compose -f docker-compose.prod.yml --profile with-nginx up --build -d; then
            echo "✅ File-Cloud is running in production mode with Nginx!"
            echo "🌐 Access your application at: http://localhost (port 80)"
            echo "🔒 For HTTPS, configure SSL certificates in the ssl/ directory"
        else
            echo "❌ Failed to start production deployment with Nginx"
            exit 1
        fi
    else
        if docker-compose -f docker-compose.prod.yml up --build -d; then
            echo "✅ File-Cloud is running in production mode!"
            echo "🌐 Access your application at: http://localhost (port 80)"
        else
            echo "❌ Failed to start production deployment"
            exit 1
        fi
    fi
    
    echo "📋 To view logs: docker-compose -f docker-compose.prod.yml logs -f"
    echo "🛑 To stop: docker-compose -f docker-compose.prod.yml down"
}

# Function to show status
show_status() {
    echo "📊 Current Docker containers status:"
    docker ps --filter "name=file-cloud"
}

# Function to show logs
show_logs() {
    echo "📋 Showing recent logs..."
    if docker ps --filter "name=file-cloud-prod" --format "{{.Names}}" | grep -q "file-cloud-prod"; then
        docker-compose -f docker-compose.prod.yml logs --tail=50 -f
    else
        docker-compose logs --tail=50 -f
    fi
}

# Function to cleanup
cleanup() {
    echo "🧹 Cleaning up Docker resources..."
    
    # Stop and remove containers
    docker-compose down 2>/dev/null || true
    docker-compose -f docker-compose.prod.yml down 2>/dev/null || true
    
    # Remove unused images
    docker image prune -f
    
    echo "✅ Cleanup completed"
}

# Main menu
show_menu() {
    echo ""
    echo "Select deployment option:"
    echo "1) 🔧 Local Development"
    echo "2) 🏭 Production"
    echo "3) 📊 Show Status"
    echo "4) 📋 Show Logs"
    echo "5) 🧹 Cleanup"
    echo "6) ❌ Exit"
    echo ""
}

# Main script
main() {
    check_docker
    
    while true; do
        show_menu
        read -p "Enter your choice (1-6): " choice
        
        case $choice in
            1)
                deploy_local
                ;;
            2)
                deploy_production
                ;;
            3)
                show_status
                ;;
            4)
                show_logs
                ;;
            5)
                cleanup
                ;;
            6)
                echo "👋 Goodbye!"
                exit 0
                ;;
            *)
                echo "❌ Invalid option. Please try again."
                ;;
        esac
        
        echo ""
        read -p "Press Enter to continue..."
    done
}

# Run main function
main