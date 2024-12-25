@echo off
echo Stopping GEEScan application...

:: Stop Docker containers (preserving them)
echo Stopping Docker containers...
docker-compose stop
echo Docker containers stopped (containers are preserved)

echo.
echo Cleaning up processes on ports 3000 and 5000...

:: Function to kill processes on a given port
:kill_port
SET port=%1
echo Checking for processes on port %port%...
FOR /F "tokens=5" %%a IN ('netstat -ano ^| find ":%port%" ^| find "LISTENING"') DO (
    echo Found process on port %port% with PID: %%a
    TASKKILL /F /PID %%a
    IF %ERRORLEVEL% EQU 0 (
        echo Successfully killed process on port %port%
    ) ELSE (
        echo Error killing process on port %port%
    )
)
EXIT /B

call :kill_port 3000
call :kill_port 5000

:: Extra check for and kill Node.js processes (more robust)
echo.
echo Cleaning up any remaining Node.js processes...
TASKLIST /FI "IMAGENAME eq node.exe" 2>nul | FIND /I /N "node.exe"
if %ERRORLEVEL% EQU 0 (
    echo Found Node.js processes. Killing them...
    TASKKILL /F /IM node.exe /T
    echo Node.js processes have been terminated.
) else (
    echo No Node.js processes found.
)

:: Wait a bit to ensure ports are fully released
echo.
echo Waiting for ports to be released...
timeout /t 3 >nul

echo.
echo GEEScan application stopped! All relevant processes terminated. Docker containers are preserved.
echo.
pause