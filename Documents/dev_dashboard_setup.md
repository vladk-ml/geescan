# Dev Dashboard Setup Guide

This guide will help you access the GEEScan development dashboard on a fresh install.

## Prerequisites

Ensure you have:
1. Run `init_containers.bat` successfully
2. PostgreSQL and PgAdmin are running
3. Set up PgAdmin connection (see pgadmin_setup.md)

## Starting the Dev Dashboard

1. Start the application:
   ```bash
   .\appstart.bat
   ```
   This will:
   - Start Docker containers if not running
   - Start the Flask backend
   - Start the frontend services

2. Access the Dev Dashboard:
   - Open your browser
   - Navigate to: http://localhost:5001/dev

## Verifying Everything Works

1. **Check System Status**
   - Click "Check All Health" button
   - All components should show "healthy":
     - API
     - Database
     - GEE (may need initialization)

2. **Initialize GEE**
   - If GEE shows "not initialized"
   - Click "Initialize GEE" button
   - Status should change to "healthy"

3. **Test AOI Creation**
   - Use the "Create New AOI" section
   - Select a preset area (e.g., "Manhattan Downtown")
   - Enter a name
   - Click "Create AOI"

## Troubleshooting

1. **Cannot Access /dev Endpoint**
   - Ensure Flask backend is running (check terminal window)
   - Verify you're using http://localhost:5000/dev
   - Check if dev.html exists in backend/app/static/

2. **Database Connection Issues**
   - Ensure PostgreSQL container is running
   - Check PgAdmin connection
   - Verify database credentials in .env file

3. **GEE Authentication Issues**
   - Ensure gee-service-account.json is present
   - Check GEE credentials are valid
   - Try reinitializing GEE

## File Locations

Important files for the dev dashboard:
- Frontend: `backend/app/static/dev.html`
- Backend Route: `backend/app/api/routes.py` (/dev endpoint)
- Styles and JavaScript: Embedded in dev.html

## Development Tips

1. To modify the dashboard:
   - Edit dev.html in the static folder
   - Changes are immediate (just refresh the browser)
   - No need to restart the server for HTML/CSS/JS changes

2. For backend changes:
   - Edit routes.py
   - Restart the Flask server to see changes
   - Use the health check buttons to verify functionality
