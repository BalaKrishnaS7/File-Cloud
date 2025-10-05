@echo off
setlocal enabledelayedexpansion

echo 🐳 File-Cloud Docker Hub Publisher
echo ==================================

REM Check if Docker is running
docker --version >nul 2>&1
if errorlevel 1 (
    echo ❌ Docker is not installed or running. Please install Docker Desktop first.
    pause
    exit /b 1
)

echo ✅ Docker is available

REM Get user input
set /p USERNAME="Enter your Docker Hub username: "
if "%USERNAME%"=="" (
    echo ❌ Username cannot be empty!
    pause
    exit /b 1
)

set /p VERSION="Enter version tag (e.g., v1.0.0) or press Enter for 'latest': "
if "%VERSION%"=="" set VERSION=latest

echo.
echo 📋 Configuration Summary:
echo    Docker Hub Username: %USERNAME%
echo    Version Tag: %VERSION%
echo    Repository: %USERNAME%/file-cloud
echo.

set /p CONFIRM="Proceed with build and push? (y/N): "
if /i not "%CONFIRM%"=="y" (
    echo ❌ Operation cancelled
    pause
    exit /b 0
)

echo.
echo 🔨 Step 1: Building Docker image...
docker build -t file-cloud .
if errorlevel 1 (
    echo ❌ Failed to build Docker image
    pause
    exit /b 1
)
echo ✅ Docker image built successfully

echo.
echo 🏷️ Step 2: Tagging image for Docker Hub...
docker tag file-cloud %USERNAME%/file-cloud:latest
if not "%VERSION%"=="latest" (
    docker tag file-cloud %USERNAME%/file-cloud:%VERSION%
)
echo ✅ Image tagged successfully

echo.
echo 🔑 Step 3: Checking Docker Hub authentication...
docker system info | findstr "Username" >nul 2>&1
if errorlevel 1 (
    echo 📝 Please login to Docker Hub:
    docker login
    if errorlevel 1 (
        echo ❌ Failed to login to Docker Hub
        pause
        exit /b 1
    )
)
echo ✅ Docker Hub authentication confirmed

echo.
echo 📤 Step 4: Pushing to Docker Hub...
echo    Pushing %USERNAME%/file-cloud:latest...
docker push %USERNAME%/file-cloud:latest
if errorlevel 1 (
    echo ❌ Failed to push latest tag
    pause
    exit /b 1
)

if not "%VERSION%"=="latest" (
    echo    Pushing %USERNAME%/file-cloud:%VERSION%...
    docker push %USERNAME%/file-cloud:%VERSION%
    if errorlevel 1 (
        echo ❌ Failed to push version tag
        pause
        exit /b 1
    )
)

echo.
echo ✅ SUCCESS! Your File-Cloud image has been published to Docker Hub!
echo.
echo 📋 Your Docker Hub repository: https://hub.docker.com/r/%USERNAME%/file-cloud
echo.
echo 🚀 Quick deployment commands:
echo    Local: docker run -d -p 5000:5000 %USERNAME%/file-cloud:latest
echo    Production: docker run -d -p 80:5000 -v uploads:/app/uploads -v db:/app/instance %USERNAME%/file-cloud:latest
echo.
echo 📄 To use in docker-compose.yml, replace 'build: .' with:
echo    image: %USERNAME%/file-cloud:latest
echo.

REM Clean up local untagged images
set /p CLEANUP="Clean up local build artifacts? (y/N): "
if /i "%CLEANUP%"=="y" (
    echo 🧹 Cleaning up...
    docker image prune -f
    echo ✅ Cleanup completed
)

echo.
echo 🎉 All done! Your File-Cloud is now available on Docker Hub.
echo.
pause