@echo off
echo Stopping application...

:: Stop Docker containers (preserving them)
echo Stopping Docker containers...
docker-compose stop
echo Docker containers stopped (containers are preserved)

echo Checking for processes on ports 3000 and 5000...

:: Find and kill process on port 3000 (React)
for /f "tokens=5" %%a in ('netstat -aon ^| find ":3000" ^| find "LISTENING"') do (
    echo Found process on port 3000 with PID: %%a
    taskkill /F /PID %%a
    if %ERRORLEVEL% EQU 0 (
        echo Successfully killed process on port 3000
    ) else (
        echo No process found on port 3000
    )
)

:: Find and kill process on port 5000 (Flask)
for /f "tokens=5" %%a in ('netstat -aon ^| find ":5000" ^| find "LISTENING"') do (
    echo Found process on port 5000 with PID: %%a
    taskkill /F /PID %%a
    if %ERRORLEVEL% EQU 0 (
        echo Successfully killed process on port 5000
    ) else (
        echo No process found on port 5000
    )
)

echo.
echo Application stopped! All ports cleared. Docker containers are preserved.
