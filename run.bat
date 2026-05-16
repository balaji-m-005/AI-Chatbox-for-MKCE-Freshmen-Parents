@echo off
echo ==========================================
echo Starting MKCE Chatbot Setup...
echo ==========================================

REM Check if Python is installed
python --version >nul 2>&1
if %errorlevel% neq 0 (
    echo [ERROR] Python is not installed or not added to your PATH.
    echo Please install Python 3.10 or newer from python.org and ensure "Add Python to PATH" is checked.
    pause
    exit /b 1
)

echo [INFO] Python is installed.
echo.

REM Setup virtual environment if it doesn't exist
if not exist .venv2 (
    echo [INFO] Creating virtual environment...
    python -m venv .venv2
) else (
    echo [INFO] Virtual environment already exists.
)

echo.
echo [INFO] Activating virtual environment...
call .venv2\Scripts\activate.bat

echo.
echo [INFO] Installing requirements...
pip install -r requirements.txt

echo.
echo [INFO] Initializing database...
python setup_initial_data.py

echo.
echo [INFO] Starting Flask Application...
echo The app will be available at http://127.0.0.1:5000/
python -m flask run

pause
