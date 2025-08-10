@echo off
echo Alumni DBMS Service Manager
echo ===========================
echo.

if "%1"=="install" goto install
if "%1"=="start" goto start
if "%1"=="stop" goto stop
if "%1"=="remove" goto remove
if "%1"=="status" goto status

echo Usage: service_manager.bat [install^|start^|stop^|remove^|status]
echo.
echo Commands:
echo   install  - Install the service
echo   start    - Start the service
echo   stop     - Stop the service
echo   remove   - Remove the service
echo   status   - Check service status
echo.
pause
exit /b

:install
echo Installing Alumni DBMS Service...
python install_service.py install
echo.
echo Service installed successfully!
echo You can now start it with: service_manager.bat start
echo.
pause
exit /b

:start
echo Starting Alumni DBMS Service...
python install_service.py start
echo.
echo Service started successfully!
echo Your app is now running at: http://10.15.5.226:5000
echo.
pause
exit /b

:stop
echo Stopping Alumni DBMS Service...
python install_service.py stop
echo.
echo Service stopped successfully!
echo.
pause
exit /b

:remove
echo Removing Alumni DBMS Service...
python install_service.py remove
echo.
echo Service removed successfully!
echo.
pause
exit /b

:status
echo Checking Alumni DBMS Service status...
python install_service.py status
echo.
pause
exit /b
