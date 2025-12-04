@echo off
REM Task & Time Manager - Windows Setup Script

echo ============================================
echo Task & Time Manager - Setup Script
echo ============================================
echo.

REM Check if Python is installed
python --version >nul 2>&1
if errorlevel 1 (
    echo ERROR: Python is not installed or not in PATH!
    echo Please install Python 3.8 or higher from python.org
    pause
    exit /b 1
)

echo Step 1: Creating virtual environment...
python -m venv venv
if errorlevel 1 (
    echo ERROR: Failed to create virtual environment!
    pause
    exit /b 1
)

echo Step 2: Activating virtual environment...
call venv\Scripts\activate.bat

echo Step 3: Upgrading pip...
python -m pip install --upgrade pip

echo Step 4: Installing dependencies...
pip install -r requirements.txt
if errorlevel 1 (
    echo ERROR: Failed to install dependencies!
    pause
    exit /b 1
)

echo Step 5: Creating database migrations...
python manage.py makemigrations
python manage.py migrate

echo.
echo ============================================
echo Setup completed successfully!
echo ============================================
echo.
echo To create an admin user, run:
echo     python manage.py createsuperuser
echo.
echo To start the server, run:
echo     python manage.py runserver
echo.
echo Then open your browser to:
echo     http://127.0.0.1:8000/
echo.
echo Admin panel available at:
echo     http://127.0.0.1:8000/admin/
echo ============================================
pause

