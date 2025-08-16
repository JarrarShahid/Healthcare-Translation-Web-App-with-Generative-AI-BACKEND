#!/bin/bash

# Railway Deployment Quick Start Script
# This script helps you get started with Railway deployment

echo "🚂 Railway Deployment Quick Start"
echo "================================"

# Check if we're in the right directory
if [ ! -f "main.py" ]; then
    echo "❌ Error: main.py not found. Please run this script from the project root directory."
    exit 1
fi

# Check if .env exists
if [ ! -f ".env" ]; then
    echo "⚠️  Warning: .env file not found. Creating from env.example..."
    if [ -f "env.example" ]; then
        cp env.example .env
        echo "✅ Created .env file from env.example"
        echo "📝 Please edit .env and add your GROQ_API_KEY"
    else
        echo "❌ env.example not found. Please create a .env file manually."
    fi
fi

# Check if GROQ_API_KEY is set
if [ -f ".env" ] && grep -q "GROQ_API_KEY=" .env; then
    echo "✅ GROQ_API_KEY found in .env"
else
    echo "⚠️  GROQ_API_KEY not found in .env"
    echo "📝 Please add GROQ_API_KEY=your_key_here to your .env file"
fi

# Check if all required files exist
echo ""
echo "📁 Checking required files for Railway deployment:"
required_files=("main.py" "requirements.txt" "railway.json" "Procfile" ".railwayignore" "runtime.txt")

for file in "${required_files[@]}"; do
    if [ -f "$file" ]; then
        echo "✅ $file"
    else
        echo "❌ $file (missing)"
    fi
done

# Test Python dependencies
echo ""
echo "🐍 Testing Python setup..."
if command -v python3 &> /dev/null; then
    echo "✅ Python 3 found: $(python3 --version)"
    
    # Check if virtual environment exists
    if [ -d "venv" ]; then
        echo "✅ Virtual environment found"
        echo "🔧 Activating virtual environment..."
        source venv/bin/activate
        
        echo "📦 Installing dependencies..."
        pip install -r requirements.txt
        
        echo "🧪 Running deployment tests..."
        python3 test_deployment.py
        
    else
        echo "⚠️  Virtual environment not found"
        echo "🔧 Creating virtual environment..."
        python3 -m venv venv
        source venv/bin/activate
        
        echo "📦 Installing dependencies..."
        pip install -r requirements.txt
        
        echo "🧪 Running deployment tests..."
        python3 test_deployment.py
    fi
else
    echo "❌ Python 3 not found. Please install Python 3.8 or higher."
    exit 1
fi

echo ""
echo "🎯 Next Steps for Railway Deployment:"
echo "1. Push your code to GitHub:"
echo "   git add ."
echo "   git commit -m 'Setup for Railway deployment'"
echo "   git push origin main"
echo ""
echo "2. Go to [railway.app](https://railway.app) and create a new project"
echo "3. Connect your GitHub repository"
echo "4. Set environment variables in Railway dashboard:"
echo "   - GROQ_API_KEY=your_actual_api_key"
echo "   - ENVIRONMENT=production"
echo "5. Deploy!"
echo ""
echo "📚 For detailed instructions, see RAILWAY_DEPLOYMENT.md"
echo "�� Happy deploying!"
