# 🚀 Quick Start Guide

Get your Healthcare Translator Backend running in 5 minutes!

## Prerequisites
- Python 3.8+ installed
- Groq API key (get one at [https://console.groq.com/](https://console.groq.com/))

## ⚡ Quick Setup (Windows)

1. **Double-click `start.bat`**
   - This will create a virtual environment, install dependencies, and start the server
   - The script will guide you through the process

## ⚡ Quick Setup (Mac/Linux)

1. **Make the script executable and run it:**
   ```bash
   chmod +x start.sh
   ./start.sh
   ```

## ⚡ Manual Setup

1. **Create virtual environment:**
   ```bash
   python -m venv venv
   
   # Windows:
   venv\Scripts\activate
   
   # Mac/Linux:
   source venv/bin/activate
   ```

2. **Install dependencies:**
   ```bash
   pip install -r requirements.txt
   ```

3. **Set up environment:**
   ```bash
   # Copy example file
   cp env.example .env
   
   # Edit .env and add your Groq API key
   GROQ_API_KEY=your_actual_api_key_here
   ```

4. **Start the server:**
   ```bash
   uvicorn main:app --reload --port 8000
   ```

## 🧪 Test Your Setup

1. **Health check:**
   ```bash
   curl http://localhost:8000/health
   ```

2. **Test translation:**
   ```bash
   curl -X POST http://localhost:8000/translate \
     -H "Content-Type: application/json" \
     -d '{"text": "I have diabetes", "source_lang": "en", "target_lang": "es"}'
   ```

3. **Or run the test script:**
   ```bash
   python test_api.py
   ```

## 🌐 API Documentation

Once running, visit: **http://localhost:8000/docs**

## 🔗 Connect Frontend

Your React frontend should now work! It's configured to connect to `http://localhost:8000/translate`.

## 🐳 Docker Option

```bash
docker-compose up --build
```

## ❗ Common Issues

- **"GROQ_API_KEY not configured"** → Check your `.env` file
- **Port already in use** → Change port in command or kill existing process
- **Import errors** → Make sure you're in the virtual environment

## 📚 Next Steps

- Read the full [README.md](README.md) for detailed information
- Test with your frontend application
- Deploy to Railway/Render for production use

---

**Need help?** Check the troubleshooting section in the main README.md

