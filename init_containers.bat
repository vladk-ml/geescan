@echo off
echo Initializing GEEScan Docker containers...

:: Check if containers already exist
docker-compose ps
echo.
set /p continue="Do you want to proceed with container setup? (Y/N): "
if /i "%continue%" neq "Y" (
    echo Setup cancelled.
    exit /b
)

:: Build and start containers in detached mode
echo Building and starting containers...
docker-compose up -d

echo.
echo Waiting for PostgreSQL to be ready...
timeout /t 15

echo.
echo Docker containers have been initialized!
echo PostgreSQL is available at localhost:5432
echo.
echo You can now use:
echo - start_app.bat to start the application
echo - clear_ports.bat to stop the application (preserves containers)
echo.
pause
