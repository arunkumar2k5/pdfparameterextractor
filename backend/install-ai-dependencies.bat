@echo off
echo ========================================
echo Installing AI Extraction Dependencies
echo ========================================
echo.

REM Activate virtual environment
call venv\Scripts\activate

echo Installing OpenAI and python-dotenv...
pip install openai>=1.0.0 python-dotenv==1.0.0

echo.
echo Updating requirements.txt...
pip freeze > requirements.txt

echo.
echo ========================================
echo Installation Complete!
echo ========================================
echo.
echo Next steps:
echo 1. Edit backend\.env and add your OpenAI API key
echo 2. Get API key from: https://platform.openai.com/api-keys
echo 3. Test connection: python openai_extractor.py
echo.
pause
