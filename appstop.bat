@echo off
echo Stopping GEEScan application...

:: Stop Docker containers (preserving them)
echo Stopping Docker containers...
docker-compose stop
echo Docker containers stopped (containers are preserved)

echo.
echo Cleaning up processes on ports 3000 and 5000...

:: Stop React development server (port 3000)
echo Checking for React development server...
FOR /F "tokens=5" %%p IN ('netstat -ano ^| findstr ":3000.*LISTENING"') DO (
    FOR /F "tokens=1" %%n IN ('tasklist /FI "PID eq %%p" ^| findstr "node.exe"') DO (
        echo Found React development server (PID: %%p). Stopping it...
        taskkill /F /PID %%p
        IF !ERRORLEVEL! EQU 0 (
            echo Successfully stopped React server
        ) ELSE (
            echo Failed to stop React server
        )
    )
)

:: Stop Flask development server (port 5000)
echo Checking for Flask development server...
FOR /F "tokens=5" %%p IN ('netstat -ano ^| findstr ":5000.*LISTENING"') DO (
    FOR /F "tokens=1" %%n IN ('tasklist /FI "PID eq %%p" ^| findstr "python.exe"') DO (
        echo Found Flask development server (PID: %%p). Stopping it...
        taskkill /F /PID %%p
        IF !ERRORLEVEL! EQU 0 (
            echo Successfully stopped Flask server
        ) ELSE (
            echo Failed to stop Flask server
        )
    )
)

echo.
echo GEEScan application stopped.