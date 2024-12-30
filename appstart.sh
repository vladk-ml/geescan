#!/bin/bash

echo "Starting GEEScan application..."

echo "Starting Docker containers..."
docker-compose start
if [ $? -ne 0 ]; then
    echo "Error starting Docker containers. Please check the Docker logs."
    exit 1
fi

echo "Docker containers started successfully!"

echo "Starting backend server..."
cd backend
source venv/bin/activate
python run.py &
cd ..

echo "Starting frontend in a new terminal..."
cd frontend
open -a Terminal "npm start"
cd ..

echo "Application startup initiated! Please wait..."
echo "Backend server is running in this console window and should be available at http://localhost:5000"
echo "Frontend is starting in a NEW TERMINAL WINDOW. Once the frontend development server is ready, it will automatically open your default web browser."
echo "PostgreSQL is available at localhost:5432"
echo "To stop the backend server, press Ctrl+C in THIS console window. The frontend server can be stopped by pressing Ctrl+C in ITS terminal window."
