@echo off
REM Railway Deployment Quick Start Script for Windows
REM This script helps you get started with Railway deployment

echo 🚂 Railway Deployment Quick Start
echo ================================

REM Check if we're in the right directory
if not exist "main.py" (
    echo ❌ Error: main.py not found. Please run this script from the project root directory.
    pause
    exit /b 1
)

REM Check if .env exists
if not exist ".env" (
    echo ⚠️  Warning: .env file not found. Creating from env.example...
    if exist "env.example" (
        copy "env.example" ".env" >nul
        echo ✅ Created .env file from env.example
        echo 📝 Please edit .env and add your GROQ_API_KEY
    ) else (
        echo ❌ env.example not found. Please create a .env file manually.
    )
)

REM Check if GROQ_API_KEY is set
findstr "GROQ_API_KEY=" .env >nul 2>&1
if %errorlevel% equ 0 (
    echo ✅ GROQ_API_KEY found in .env
) else (
    echo ⚠️  GROQ_API_KEY not found in .env
    echo 📝 Please add GROQ_API_KEY=your_key_here to your .env file
)

REM Check if all required files exist
echo.
echo 📁 Checking required files for Railway deployment:
set "required_files=main.py requirements.txt railway.json Procfile .railwayignore runtime.txt"

for %%f in (%required_files%) do (
    if exist "%%f" (
        echo ✅ %%f
    ) else (
        echo ❌ %%f (missing)
    )
)

REM Test Python dependencies
echo.
echo 🐍 Testing Python setup...
python --version >nul 2>&1
if %errorlevel% equ 0 (
    echo ✅ Python found: 
    python --version
    
    REM Check if virtual environment exists
    if exist "venv" (
        echo ✅ Virtual environment found
        echo 🔧 Activating virtual environment...
        call venv\Scripts\activate.bat
        
        echo 📦 Installing dependencies...
        pip install -r requirements.txt
        
        echo 🧪 Running deployment tests...
        python test_deployment.py
        
    ) else (
        echo ⚠️  Virtual environment not found
        echo 🔧 Creating virtual environment...
        python -m venv venv
        call venv\Scripts\activate.bat
        
        echo 📦 Installing dependencies...
        pip install -r requirements.txt
        
        echo 🧪 Running deployment tests...
        python test_deployment.py
    )
) else (
    echo ❌ Python not found. Please install Python 3.8 or higher.
    pause
    exit /b 1
)

echo.
echo 🎯 Next Steps for Railway Deployment:
echo 1. Push your code to GitHub:
echo    git add .
echo    git commit -m "Setup for Railway deployment"
echo    git push origin main
echo.
echo 2. Go to https://railway.app and create a new project
echo 3. Connect your GitHub repository
echo 4. Set environment variables in Railway dashboard:
echo    - GROQ_API_KEY=your_actual_api_key
echo    - ENVIRONMENT=production
echo 5. Deploy!
echo.
echo 📚 For detailed instructions, see RAILWAY_DEPLOYMENT.md
echo 🚀 Happy deploying!

pause
