@echo off
echo Starting GEEScan application...

:: Start Docker containers
echo Starting Docker containers...
docker-compose start
timeout /t 10
echo Docker containers started!

:: Activate virtual environment and start backend
echo Starting backend server...
cd backend
call venv\Scripts\activate
start cmd /k "python run.py"

:: Wait a bit for backend to initialize
timeout /t 5

:: Start frontend
echo Starting frontend...
cd ../frontend
start cmd /k "npm start"

echo.
echo Application starting! Please wait...
echo Backend will be available at http://localhost:5000
echo Frontend will be available at http://localhost:3000
echo PostgreSQL is available at localhost:5432
