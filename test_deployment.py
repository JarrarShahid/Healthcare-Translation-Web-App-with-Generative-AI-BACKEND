#!/usr/bin/env python3
"""
Test script to verify Railway deployment setup
Run this locally to test your application before deploying
"""

import os
import sys
import requests
import time
from dotenv import load_dotenv

# Load environment variables
load_dotenv()

def test_environment():
    """Test environment variable loading"""
    print("🔍 Testing environment variables...")
    
    groq_key = os.getenv("GROQ_API_KEY")
    if groq_key:
        print("✅ GROQ_API_KEY loaded successfully")
        print(f"   Key length: {len(groq_key)} characters")
    else:
        print("❌ GROQ_API_KEY not found")
        print("   Please set it in your .env file or Railway environment variables")
        return False
    
    return True

def test_imports():
    """Test if all required packages can be imported"""
    print("\n📦 Testing package imports...")
    
    try:
        import fastapi
        print("✅ FastAPI imported successfully")
    except ImportError as e:
        print(f"❌ FastAPI import failed: {e}")
        return False
    
    try:
        import uvicorn
        print("✅ Uvicorn imported successfully")
    except ImportError as e:
        print(f"❌ Uvicorn import failed: {e}")
        return False
    
    try:
        import langchain
        print("✅ LangChain imported successfully")
    except ImportError as e:
        print(f"❌ LangChain import failed: {e}")
        return False
    
    try:
        import groq
        print("✅ Groq imported successfully")
    except ImportError as e:
        print(f"❌ Groq import failed: {e}")
        return False
    
    return True

def test_app_creation():
    """Test if the FastAPI app can be created"""
    print("\n🚀 Testing FastAPI app creation...")
    
    try:
        # Import the app
        from main import app
        
        print("✅ FastAPI app created successfully")
        print(f"   App title: {app.title}")
        print(f"   App version: {app.version}")
        
        # Check routes
        routes = [route.path for route in app.routes]
        print(f"   Available routes: {routes}")
        
        return True
    except Exception as e:
        print(f"❌ App creation failed: {e}")
        return False

def test_health_endpoint():
    """Test the health endpoint"""
    print("\n🏥 Testing health endpoint...")
    
    try:
        from main import app
        import uvicorn
        import threading
        
        # Start server in background
        def run_server():
            uvicorn.run(app, host="127.0.0.1", port=8001, log_level="error")
        
        server_thread = threading.Thread(target=run_server, daemon=True)
        server_thread.start()
        
        # Wait for server to start
        time.sleep(3)
        
        # Test health endpoint
        response = requests.get("http://127.0.0.1:8001/health", timeout=5)
        
        if response.status_code == 200:
            print("✅ Health endpoint working")
            print(f"   Response: {response.json()}")
        else:
            print(f"❌ Health endpoint failed with status {response.status_code}")
            return False
        
        return True
        
    except Exception as e:
        print(f"❌ Health endpoint test failed: {e}")
        return False

def main():
    """Run all tests"""
    print("🚂 Railway Deployment Test Suite")
    print("=" * 40)
    
    tests = [
        ("Environment Variables", test_environment),
        ("Package Imports", test_imports),
        ("App Creation", test_app_creation),
        ("Health Endpoint", test_health_endpoint),
    ]
    
    passed = 0
    total = len(tests)
    
    for test_name, test_func in tests:
        try:
            if test_func():
                passed += 1
            else:
                print(f"❌ {test_name} test failed")
        except Exception as e:
            print(f"❌ {test_name} test crashed: {e}")
    
    print("\n" + "=" * 40)
    print(f"📊 Test Results: {passed}/{total} tests passed")
    
    if passed == total:
        print("🎉 All tests passed! Your app is ready for Railway deployment.")
        print("\nNext steps:")
        print("1. Push your code to GitHub")
        print("2. Connect your repository to Railway")
        print("3. Set GROQ_API_KEY in Railway environment variables")
        print("4. Deploy!")
    else:
        print("⚠️  Some tests failed. Please fix the issues before deploying.")
        return 1
    
    return 0

if __name__ == "__main__":
    sys.exit(main())
