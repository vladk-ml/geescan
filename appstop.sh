#!/bin/bash

echo "Stopping GEEScan application..."

echo "Stopping Docker containers..."
docker-compose stop

echo "Docker containers stopped (containers are preserved)"
echo "Cleaning up processes on ports 3000 and 5000..."

echo "Checking for React development server..."
PID=$(lsof -ti:3000)
if [ -n "$PID" ]; then
    echo "Found React development server (PID: $PID). Stopping it..."
    kill -9 $PID
    echo "Successfully stopped React server"
else
    echo "No React server found"
fi

echo "Checking for Flask development server..."
PID=$(lsof -ti:5001)
if [ -n "$PID" ]; then
    echo "Found Flask development server (PID: $PID). Stopping it..."
    kill -9 $PID
    echo "Successfully stopped Flask server"
else
    echo "No Flask server found"
fi

echo "GEEScan application stopped."
