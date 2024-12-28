@echo off
echo Stopping GEEScan application...

:: Stop Docker containers (preserving them)
echo Stopping Docker containers...
docker-compose stop
echo Docker containers stopped (containers are preserved)

echo.
echo Cleaning up processes on ports 3000 and 5000...

:: Function to kill processes on a given port with confirmation
:kill_port
SET port=%1
echo Checking for processes on port %port%...
FOR /F "tokens=5" %%a IN ('netstat -ano ^| find ":%port%" ^| find "LISTENING"') DO (
    echo Found process on port %port% with PID: %%a
    :: Get process name for verification
    FOR /F "tokens=1" %%b IN ('tasklist /FI "PID eq %%a" ^| findstr /i "node.exe python.exe"') DO (
        echo Process name: %%b
        TASKKILL /F /PID %%a
        IF !ERRORLEVEL! EQU 0 (
            echo Successfully killed process on port %port%
        ) ELSE (
            echo Error killing process on port %port%
        )
    )
)
EXIT /B

call :kill_port 3000
call :kill_port 5000

:: Check specifically for React development server
echo.
echo Checking for React development server...
FOR /F "tokens=2" %%p IN ('netstat -ano ^| find ":3000" ^| find "LISTENING"') DO (
    FOR /F "tokens=1" %%n IN ('tasklist /FI "PID eq %%p" ^| findstr "node.exe"') DO (
        echo Found React development server. Stopping it...
        TASKKILL /F /PID %%p
    )
)

:: Check specifically for Flask development server
echo.
echo Checking for Flask development server...
FOR /F "tokens=2" %%p IN ('netstat -ano ^| find ":5000" ^| find "LISTENING"') DO (
    FOR /F "tokens=1" %%n IN ('tasklist /FI "PID eq %%p" ^| findstr "python.exe"') DO (
        echo Found Flask development server. Stopping it...
        TASKKILL /F /PID %%p
    )
)

:: Wait a bit to ensure ports are fully released
echo.
echo Waiting for ports to be released...
timeout /t 3 >nul

echo.
echo GEEScan application stopped! All relevant processes terminated. Docker containers are preserved.
echo.
pause