@echo off
setlocal enabledelayedexpansion

REM File-Cloud Docker Deployment Script for Windows
REM This script helps you deploy File-Cloud with Docker quickly

echo 🐳 File-Cloud Docker Deployment Script
echo ======================================

:check_docker
echo Checking Docker installation...
docker --version >nul 2>&1
if errorlevel 1 (
    echo ❌ Docker is not installed. Please install Docker Desktop first.
    echo Visit: https://docs.docker.com/desktop/windows/
    pause
    exit /b 1
)

docker-compose --version >nul 2>&1
if errorlevel 1 (
    docker compose version >nul 2>&1
    if errorlevel 1 (
        echo ❌ Docker Compose is not installed. Please install Docker Compose first.
        pause
        exit /b 1
    )
)

echo ✅ Docker and Docker Compose are installed

:create_directories
echo 📁 Creating necessary directories...
if not exist "uploads" mkdir uploads
if not exist "instance" mkdir instance
if not exist "ssl" mkdir ssl
echo ✅ Directories created

:main_menu
echo.
echo Select deployment option:
echo 1^) 🔧 Local Development
echo 2^) 🏭 Production
echo 3^) 📊 Show Status
echo 4^) 📋 Show Logs
echo 5^) 🧹 Cleanup
echo 6^) ❌ Exit
echo.

set /p choice="Enter your choice (1-6): "

if "%choice%"=="1" goto deploy_local
if "%choice%"=="2" goto deploy_production
if "%choice%"=="3" goto show_status
if "%choice%"=="4" goto show_logs
if "%choice%"=="5" goto cleanup
if "%choice%"=="6" goto exit_script
echo ❌ Invalid option. Please try again.
goto main_menu

:deploy_local
echo 🚀 Starting local development deployment...
call :create_directories

docker-compose up --build -d
if errorlevel 1 (
    echo ❌ Failed to start local deployment
    pause
    goto main_menu
)

echo ✅ File-Cloud is running in development mode!
echo 🌐 Access your application at: http://localhost:5000
echo 📋 To view logs: docker-compose logs -f
echo 🛑 To stop: docker-compose down
goto continue_prompt

:deploy_production
echo 🚀 Starting production deployment...
call :create_directories

set /p include_nginx="Do you want to include Nginx reverse proxy? (y/N): "

if /i "%include_nginx%"=="y" (
    docker-compose -f docker-compose.prod.yml --profile with-nginx up --build -d
    if errorlevel 1 (
        echo ❌ Failed to start production deployment with Nginx
        pause
        goto main_menu
    )
    echo ✅ File-Cloud is running in production mode with Nginx!
    echo 🌐 Access your application at: http://localhost (port 80)
    echo 🔒 For HTTPS, configure SSL certificates in the ssl/ directory
) else (
    docker-compose -f docker-compose.prod.yml up --build -d
    if errorlevel 1 (
        echo ❌ Failed to start production deployment
        pause
        goto main_menu
    )
    echo ✅ File-Cloud is running in production mode!
    echo 🌐 Access your application at: http://localhost (port 80)
)

echo 📋 To view logs: docker-compose -f docker-compose.prod.yml logs -f
echo 🛑 To stop: docker-compose -f docker-compose.prod.yml down
goto continue_prompt

:show_status
echo 📊 Current Docker containers status:
docker ps --filter "name=file-cloud"
goto continue_prompt

:show_logs
echo 📋 Showing recent logs...
docker ps --filter "name=file-cloud-prod" --format "{{.Names}}" | findstr "file-cloud-prod" >nul
if not errorlevel 1 (
    docker-compose -f docker-compose.prod.yml logs --tail=50 -f
) else (
    docker-compose logs --tail=50 -f
)
goto continue_prompt

:cleanup
echo 🧹 Cleaning up Docker resources...

REM Stop and remove containers
docker-compose down 2>nul
docker-compose -f docker-compose.prod.yml down 2>nul

REM Remove unused images
docker image prune -f

echo ✅ Cleanup completed
goto continue_prompt

:continue_prompt
echo.
pause
goto main_menu

:exit_script
echo 👋 Goodbye!
pause
exit /b 0