#!/bin/bash

echo "Starting Healthcare Translator Backend..."
echo

# Check if virtual environment exists
if [ ! -d "venv" ]; then
    echo "Creating virtual environment..."
    python3 -m venv venv
    echo "Virtual environment created."
    echo
fi

# Activate virtual environment
echo "Activating virtual environment..."
source venv/bin/activate

# Install dependencies if requirements.txt exists
if [ -f "requirements.txt" ]; then
    echo "Installing dependencies..."
    pip install -r requirements.txt
    echo "Dependencies installed."
    echo
fi

# Check if .env file exists
if [ ! -f ".env" ]; then
    echo "Warning: .env file not found!"
    echo "Please create .env file with your GROQ_API_KEY"
    echo "Copy env.example to .env and add your API key"
    echo
    read -p "Press Enter to continue anyway..."
fi

# Start the server
echo "Starting server on http://localhost:8000..."
echo "Press Ctrl+C to stop the server"
echo
uvicorn main:app --reload --port 8000

