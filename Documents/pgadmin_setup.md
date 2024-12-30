# PgAdmin Setup Guide

This guide will help you connect PgAdmin to your PostgreSQL database in the GEEScan development environment.

## 1. Access PgAdmin

1. Start your containers using `init_containers.bat`
2. Open your web browser and navigate to: http://localhost:5050
3. Login credentials:
   - Email: admin@geescan.com
   - Password: admin

## 2. Add New Server Connection

1. Right-click on "Servers" in the left sidebar
2. Select "Register" → "Server"
3. In the "General" tab:
   - Name: GEEScan (or any name you prefer)

4. In the "Connection" tab:
   - Host name/address: `postgres` (Important: Use this, not `postgres-1` or `localhost`)
   - Port: `5432`
   - Maintenance database: `geescan`
   - Username: `geescan`
   - Password: `geescan`
   - Save password: Yes (for development convenience)

## 3. Verify Connection

1. After saving, expand your new server in the left sidebar
2. Navigate to: Servers → GEEScan → Databases → geescan → Schemas → public → Tables
3. You should see the following tables:
   - aois
   - export_tasks

## Common Issues

1. **Connection Refused Error**
   - If you get "could not connect to server: Connection refused", make sure:
     - Docker containers are running (`docker ps`)
     - You're using `postgres` as the hostname (not `postgres-1` or `localhost`)

2. **Authentication Failed**
   - Double-check the credentials in docker-compose.yml match what you're using
   - Default credentials are:
     ```
     Username: geescan
     Password: geescan
     ```

3. **Can't See Tables**
   - Refresh the browser
   - Disconnect and reconnect the server
   - Check if init.sql was properly mounted and executed

## Why `postgres` and not `postgres-1`?

While Docker Compose names the container `geescan-postgres-1`, within the Docker network, the service is accessible by its service name `postgres` as defined in docker-compose.yml. This is a Docker networking feature that allows containers to communicate using service names.
