@echo off
echo Starting GEEScan application...

:: Start Docker containers and check for errors
echo Starting Docker containers...
docker-compose start
if %errorlevel% neq 0 (
    echo Error starting Docker containers. Please check the Docker logs.
    pause
    exit /b
)
echo Docker containers started successfully!

:: Activate virtual environment and start backend in the same window
echo Starting backend server...
cd backend
call venv\Scripts\activate
python run.py
cd ..

:: Start frontend in a separate terminal and explicitly mention how to find the URL
echo Starting frontend in a new command prompt window...
cd frontend
start cmd /k "npm start"
cd ..

echo.
echo Application startup initiated! Please wait...
echo.
echo Backend server is running in this console window and should be available at http://localhost:5000
echo.
echo Frontend is starting in a NEW COMMAND PROMPT WINDOW. 
echo Once the frontend development server is ready, it will automatically open your default web browser.
echo Alternatively, check the output in the new frontend command prompt window for the exact URL (likely http://localhost:3000 or similar).
echo.
echo PostgreSQL is available at localhost:5432

echo.
echo To stop the backend server, press Ctrl+C in THIS console window.
echo The frontend server can be stopped by pressing Ctrl+C in ITS command prompt window.

pause