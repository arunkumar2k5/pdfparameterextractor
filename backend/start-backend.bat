@echo off
echo ========================================
echo Starting Backend Server
echo ========================================
echo.
echo Checking Python environment...
python --version
echo.
echo Installing/Updating dependencies...
pip install -r requirements.txt
echo.
echo Starting FastAPI server on http://localhost:8000
echo Press Ctrl+C to stop the server
echo ========================================
echo.
python main.py
