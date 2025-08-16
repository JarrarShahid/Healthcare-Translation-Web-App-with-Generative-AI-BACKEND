#!/usr/bin/env python3
"""
Railway startup script for Healthcare Translator Backend
This script ensures proper startup and environment configuration
"""

import os
import sys
import logging
from dotenv import load_dotenv

# Configure logging
logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s'
)
logger = logging.getLogger(__name__)

def check_environment():
    """Check if required environment variables are set"""
    logger.info("🔍 Checking environment variables...")
    
    # Check GROQ_API_KEY
    groq_key = os.getenv("GROQ_API_KEY")
    if not groq_key:
        logger.error("❌ GROQ_API_KEY not found in environment variables")
        logger.error("Please set GROQ_API_KEY in Railway environment variables")
        return False
    
    logger.info("✅ GROQ_API_KEY found")
    
    # Check PORT
    port = os.getenv("PORT", "8000")
    logger.info(f"✅ PORT set to: {port}")
    
    # Check environment
    env = os.getenv("ENVIRONMENT", "production")
    logger.info(f"✅ Environment: {env}")
    
    return True

def main():
    """Main startup function"""
    logger.info("🚂 Starting Healthcare Translator Backend for Railway...")
    
    # Load environment variables
    load_dotenv()
    
    # Check environment
    if not check_environment():
        logger.error("❌ Environment check failed. Exiting...")
        sys.exit(1)
    
    try:
        # Import and start the app
        import uvicorn
        from main import app
        
        # Get configuration
        host = os.getenv("HOST", "0.0.0.0")
        port = int(os.getenv("PORT", 8000))
        
        logger.info(f"🚀 Starting server on {host}:{port}")
        logger.info("✅ All systems ready for deployment!")
        
        # Start the server
        uvicorn.run(
            "main:app",
            host=host,
            port=port,
            reload=False,  # Disable reload in production
            log_level="info"
        )
        
    except ImportError as e:
        logger.error(f"❌ Import error: {e}")
        logger.error("Please ensure all dependencies are installed")
        sys.exit(1)
    except Exception as e:
        logger.error(f"❌ Startup error: {e}")
        sys.exit(1)

if __name__ == "__main__":
    main()
