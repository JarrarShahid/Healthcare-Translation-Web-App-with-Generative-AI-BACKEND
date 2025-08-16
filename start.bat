@echo off
echo Starting Healthcare Translator Backend...
echo.

REM Check if virtual environment exists
if not exist "venv" (
    echo Creating virtual environment...
    python -m venv venv
    echo Virtual environment created.
    echo.
)

REM Activate virtual environment
echo Activating virtual environment...
call venv\Scripts\activate

REM Install dependencies if requirements.txt exists
if exist "requirements.txt" (
    echo Installing dependencies...
    pip install -r requirements.txt
    echo Dependencies installed.
    echo.
)

REM Check if .env file exists
if not exist ".env" (
    echo Warning: .env file not found!
    echo Please create .env file with your GROQ_API_KEY
    echo Copy env.example to .env and add your API key
    echo.
    pause
)

REM Start the server
echo Starting server on http://localhost:8000...
echo Press Ctrl+C to stop the server
echo.
uvicorn main:app --reload --port 8000

pause

