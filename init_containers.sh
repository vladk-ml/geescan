#!/bin/bash

echo "Initializing GEEScan containers..."

# Check if Docker is running
if ! docker info > /dev/null 2>&1; then
    echo "Docker is not running. Please start Docker Desktop and try again."
    exit 1
fi

# Create Docker network if it doesn't exist
docker network create geescan-network 2>/dev/null || true

# Start containers with docker-compose
echo "Starting containers with docker-compose..."
docker-compose up -d

# Wait for PostgreSQL to be ready
echo "Waiting for PostgreSQL to be ready..."
while ! docker exec geescan-postgres-1 pg_isready -h localhost -p 5432 > /dev/null 2>&1; do
    echo -n "."
    sleep 1
done

echo ""
echo "Containers initialized successfully!"
echo "PostgreSQL is available at: localhost:5432"
echo "PgAdmin is available at: http://localhost:5050"
echo "You can now run appstart.sh to start the application"
