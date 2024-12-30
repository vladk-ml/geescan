@echo off
echo Initializing GEEScan containers...

:: Check if Docker is running
docker info > nul 2>&1
if %errorlevel% neq 0 (
    echo Docker is not running. Please start Docker Desktop and try again.
    pause
    exit /b
)

:: Create Docker network if it doesn't exist
docker network create geescan-network 2>nul || ver>nul

:: Start containers with docker-compose
echo Starting containers with docker-compose...
docker-compose up -d

:: Wait for PostgreSQL to be ready
echo Waiting for PostgreSQL to be ready...
:check_postgres
docker exec geescan-postgres-1 pg_isready -h localhost -p 5432 > nul 2>&1
if %errorlevel% neq 0 (
    echo|set /p=".."
    timeout /t 1 /nobreak > nul
    goto check_postgres
)
echo.

echo Containers initialized successfully!
echo.
echo PostgreSQL is available at: localhost:5432
echo PgAdmin is available at: http://localhost:5050
echo.
echo You can now run appstart.bat to start the application
