@echo off
REM Weather Dashboard Quick Start
REM Run this file to start the production server

echo.
echo Weather API Dashboard - Production Server
echo =========================================
echo.

cd /d "%~dp0"

REM Activate virtual environment
call .\.venv\Scripts\activate.bat

REM Start production server
python -m waitress --port=8000 --threads=4 app_production:app
