#!/usr/bin/env python3
"""
CORS Testing Script for Healthcare Translator Backend
This script tests CORS functionality from different origins
"""

import requests
import json
import sys
from urllib.parse import urlparse

def test_cors_request(url, origin, method="GET", endpoint="/cors-test", data=None):
    """Test CORS request with specific origin"""
    headers = {
        "Origin": origin,
        "Content-Type": "application/json" if data else "text/plain"
    }
    
    try:
        if method == "GET":
            response = requests.get(f"{url}{endpoint}", headers=headers)
        elif method == "POST":
            response = requests.post(f"{url}{endpoint}", headers=headers, json=data)
        elif method == "OPTIONS":
            response = requests.options(f"{url}{endpoint}", headers=headers)
        
        print(f"✅ {method} {endpoint} from {origin}")
        print(f"   Status: {response.status_code}")
        print(f"   CORS Headers:")
        
        # Check CORS headers
        cors_headers = {
            "Access-Control-Allow-Origin": response.headers.get("Access-Control-Allow-Origin"),
            "Access-Control-Allow-Methods": response.headers.get("Access-Control-Allow-Methods"),
            "Access-Control-Allow-Headers": response.headers.get("Access-Control-Allow-Headers"),
            "Access-Control-Max-Age": response.headers.get("Access-Control-Max-Age")
        }
        
        for header, value in cors_headers.items():
            if value:
                print(f"     {header}: {value}")
            else:
                print(f"     {header}: ❌ Missing")
        
        if response.status_code == 200:
            try:
                print(f"   Response: {response.json()}")
            except:
                print(f"   Response: {response.text}")
        else:
            print(f"   Error Response: {response.text}")
            
        return True
        
    except Exception as e:
        print(f"❌ {method} {endpoint} from {origin} - Error: {e}")
        return False

def main():
    """Main testing function"""
    print("🌐 CORS Testing for Healthcare Translator Backend")
    print("=" * 60)
    
    # Get backend URL
    if len(sys.argv) > 1:
        backend_url = sys.argv[1].rstrip('/')
    else:
        backend_url = "http://localhost:8000"
    
    print(f"Testing backend at: {backend_url}")
    print()
    
    # Test origins
    test_origins = [
        "http://localhost:3000",
        "http://localhost:5173", 
        "https://example.vercel.app",
        "https://myapp.vercel.app",
        "https://web-production-707fbe.up.railway.app"
    ]
    
    # Test endpoints
    test_endpoints = [
        ("/cors-test", "GET"),
        ("/health", "GET"),
        ("/translate", "OPTIONS"),
        ("/translate", "POST", {"text": "Hello", "source_lang": "en", "target_lang": "es"})
    ]
    
    results = []
    
    for endpoint_info in test_endpoints:
        endpoint = endpoint_info[0]
        method = endpoint_info[1]
        data = endpoint_info[2] if len(endpoint_info) > 2 else None
        
        print(f"🔍 Testing {method} {endpoint}")
        print("-" * 40)
        
        for origin in test_origins:
            success = test_cors_request(backend_url, origin, method, endpoint, data)
            results.append((origin, endpoint, method, success))
            print()
        
        print("=" * 60)
        print()
    
    # Summary
    print("📊 CORS Test Summary")
    print("=" * 60)
    
    total_tests = len(results)
    successful_tests = sum(1 for _, _, _, success in results if success)
    
    print(f"Total Tests: {total_tests}")
    print(f"Successful: {successful_tests}")
    print(f"Failed: {total_tests - successful_tests}")
    
    if successful_tests == total_tests:
        print("🎉 All CORS tests passed!")
    else:
        print("⚠️  Some CORS tests failed. Check the configuration.")
    
    print()
    print("💡 Tips:")
    print("- Ensure your backend is running")
    print("- Check that CORS middleware is properly configured")
    print("- Verify environment variables are set correctly")
    print("- Test with your actual Vercel domain")

if __name__ == "__main__":
    main()
