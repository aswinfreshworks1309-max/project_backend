@echo off
echo ============================================================
echo RUNNING BUS POPULATION SCRIPT
echo ============================================================
echo.
cd /d "c:\Project Version 1\project_backend"
echo Current directory: %CD%
echo.
echo Activating virtual environment...
call Backend\Scripts\activate.bat
echo.
echo Running populate_buses.py...
echo.
python populate_buses.py
echo.
echo ============================================================
echo Script execution completed
echo ============================================================
pause
