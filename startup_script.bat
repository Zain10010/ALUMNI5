@echo off
cd /d "%~dp0"
echo Starting Alumni DBMS Application...
echo.
echo This script will start your Flask application and keep it running.
echo To stop the application, close this window.
echo.
echo Your app will be available at: http://10.15.5.226:5000
echo.
echo Press any key to start...
pause >nul

:start_loop
echo Starting Flask application...
python app.py
echo.
echo Application stopped or crashed. Restarting in 5 seconds...
timeout /t 5 /nobreak >nul
goto start_loop
