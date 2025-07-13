@echo off
title Enhanced Voice Assistant
echo Starting Enhanced Voice Assistant...
echo =====================================

REM Activate virtual environment if it exists
if exist "venv\Scripts\activate.bat" (
    echo Activating virtual environment...
    call venv\Scripts\activate.bat
) else (
    echo Warning: Virtual environment not found. Using system Python...
)

REM Install dependencies if needed
echo Checking dependencies...
python -m pip install -r requirements.txt --quiet

REM Start the enhanced voice assistant
echo Starting Enhanced Voice Assistant...
echo =====================================
python enhanced_voice_assistant.py

REM Keep window open if there's an error
if %errorlevel% neq 0 (
    echo.
    echo An error occurred. Press any key to exit...
    pause > nul
)
