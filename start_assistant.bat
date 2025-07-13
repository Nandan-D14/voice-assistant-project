@echo off
echo Starting Voice Assistant...
echo.
echo Make sure you have:
echo 1. Set your GEMINI_API_KEY in the .env file
echo 2. A working microphone
echo 3. Speakers or headphones
echo.
pause
call venv\Scripts\activate
python voice_assistant.py
pause
