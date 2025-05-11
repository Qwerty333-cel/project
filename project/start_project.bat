@echo off
echo Starting Django Project...

:: Change to the project directory
cd /d %~dp0

:: Clear port 5432 for PostgreSQL
echo Clearing port 5432...
call port_clearer.bat

:: Create virtual environment if it doesn't exist
if not exist venv (
    echo Creating virtual environment...
    python -m venv venv
)

:: Activate virtual environment
echo Activating virtual environment...
call venv\Scripts\activate

:: Install dependencies
echo Installing dependencies...
pip install -r requirements.txt

:: Check if Docker Desktop is running
docker info > nul 2>&1
if errorlevel 1 (
    echo Docker Desktop is not running. Starting Docker Desktop...
    start "" "C:\Program Files\Docker\Docker\Docker Desktop.exe"
    echo Waiting for Docker to start...
    timeout /t 30 
)

:: Stop any running containers
echo Stopping any running containers...
cmd /c docker-compose down

:: Remove old containers and volumes
echo Cleaning up old containers and volumes...
cmd /c docker-compose down -v
cmd /c docker system prune -f

:: Build and start containers
echo Building and starting containers...
cmd /c docker-compose build --no-cache
cmd /c docker-compose up -d

:: Wait for services to be ready
echo Waiting for services to be ready...
timeout /t 10 /nobreak

:: Check container status
echo.
echo Checking container status...
cmd /c docker-compose ps

:: Show logs if there are issues
echo.
echo Checking container logs...
cmd /c docker-compose logs web

echo.
echo Project is running!
echo Django app: http://localhost:8000
echo PgAdmin: http://localhost:5050
echo.
echo Press any key to stop the containers...
pause > nul

:: Stop containers
cmd /c docker-compose down

:: Deactivate virtual environment
deactivate 