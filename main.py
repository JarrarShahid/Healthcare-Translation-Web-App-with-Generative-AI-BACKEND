from fastapi import FastAPI, HTTPException
from fastapi.middleware.cors import CORSMiddleware
from pydantic import BaseModel
from langchain_groq import ChatGroq
from langchain.schema import HumanMessage
from langchain.prompts import ChatPromptTemplate
from dotenv import load_dotenv
import os
import logging

# Load environment variables
load_dotenv()

# Configure logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

# Debug: Check if .env is loaded
logger.info(f"GROQ_API_KEY loaded: {'Yes' if os.getenv('GROQ_API_KEY') else 'No'}")

# Initialize FastAPI app
app = FastAPI(
    title="Healthcare Translator API",
    description="AI-powered medical translation service using Groq LLM",
    version="1.0.0"
)

@app.on_event("startup")
async def startup_event():
    """Run on app startup"""
    logger.info("🚀 Healthcare Translator API starting up...")
    logger.info(f"Environment: {os.getenv('ENVIRONMENT', 'development')}")
    logger.info(f"Port: {os.getenv('PORT', '8000')}")
    logger.info("✅ App startup complete")

# Add CORS middleware for frontend integration
app.add_middleware(
    CORSMiddleware,
    allow_origins=[
        "http://localhost:3000", 
        "http://localhost:5173", 
        "http://127.0.0.1:3000", 
        "http://127.0.0.1:5173",
        # Add Railway domains
        "https://*.railway.app",
        "https://*.up.railway.app"
    ],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Pydantic models for request/response
class TranslationRequest(BaseModel):
    text: str
    source_lang: str
    target_lang: str

class TranslationResponse(BaseModel):
    translated_text: str

class ErrorResponse(BaseModel):
    error: str

# Initialize Groq client
def get_groq_client():
    api_key = os.getenv("GROQ_API_KEY")
    
    if not api_key:
        logger.error("GROQ_API_KEY not found in environment variables")
        raise HTTPException(
            status_code=500,
            detail="GROQ_API_KEY not configured. Please set it in your .env file."
        )
    
    return ChatGroq(
        groq_api_key=api_key,
        model_name="llama3-8b-8192",  # Using LLaMA3-8B (fast and reliable)
        temperature=0.1  # Low temperature for consistent medical translations
    )

# Medical translation prompt template
MEDICAL_TRANSLATION_PROMPT = ChatPromptTemplate.from_template(
    """You are a professional medical translation assistant with expertise in healthcare terminology.

Your task is to translate medical text from {source_lang} to {target_lang}.

IMPORTANT GUIDELINES:
- Preserve and accurately translate ALL medical terminology
- Maintain the medical context and meaning
- Use appropriate medical vocabulary in the target language
- Keep the translation clear and understandable for healthcare professionals
- If a medical term doesn't have a direct translation, provide the closest equivalent
- Maintain the same level of formality as the original text

Source Language: {source_lang}
Target Language: {target_lang}
Text to translate: {text}

Provide ONLY the translated text without any explanations or additional text."""
)

@app.get("/")
async def root():
    """Health check endpoint"""
    return {
        "message": "Healthcare Translator API",
        "status": "running",
        "version": "1.0.0"
    }

@app.get("/health")
async def health_check():
    """Health check endpoint for Railway"""
    try:
        # Quick check if Groq API key is available
        api_key = os.getenv("GROQ_API_KEY")
        if not api_key:
            return {"status": "unhealthy", "error": "GROQ_API_KEY not configured"}
        
        return {"status": "healthy", "timestamp": "2024-01-01T00:00:00Z"}
    except Exception as e:
        return {"status": "unhealthy", "error": str(e)}

@app.get("/ready")
async def readiness_check():
    """Readiness check endpoint for Railway"""
    return {"status": "ready", "service": "healthcare-translator"}

@app.post("/translate", response_model=TranslationResponse, responses={400: {"model": ErrorResponse}, 500: {"model": ErrorResponse}})
async def translate_text(request: TranslationRequest):
    """
    Translate medical text from one language to another using AI.
    
    - **text**: The medical text to translate
    - **source_lang**: Source language code (e.g., 'en', 'es', 'fr')
    - **target_lang**: Target language code (e.g., 'es', 'en', 'de')
    """
    try:
        # Validate input
        if not request.text.strip():
            raise HTTPException(status_code=400, detail="Text cannot be empty")
        
        if not request.source_lang or not request.target_lang:
            raise HTTPException(status_code=400, detail="Source and target languages are required")
        
        # Get Groq client
        groq_client = get_groq_client()
        
        # Prepare the prompt
        messages = MEDICAL_TRANSLATION_PROMPT.format_messages(
            source_lang=request.source_lang,
            target_lang=request.target_lang,
            text=request.text
        )
        
        # Call Groq API
        logger.info(f"Translating from {request.source_lang} to {request.target_lang}")
        response = groq_client.invoke(messages)
        
        # Extract translated text
        translated_text = response.content.strip()
        
        if not translated_text:
            raise HTTPException(status_code=500, detail="Translation failed - empty response from AI model")
        
        logger.info(f"Translation successful: {len(request.text)} chars -> {len(translated_text)} chars")
        
        return TranslationResponse(translated_text=translated_text)
        
    except HTTPException:
        # Re-raise HTTP exceptions
        raise
    except Exception as e:
        logger.error(f"Translation error: {str(e)}")
        raise HTTPException(
            status_code=500,
            detail="Translation failed, please try again."
        )

@app.get("/languages")
async def get_supported_languages():
    """Get list of supported languages for translation"""
    return {
        "languages": [
            {"code": "en", "name": "English"},
            {"code": "es", "name": "Spanish"},
            {"code": "fr", "name": "French"},
            {"code": "de", "name": "German"},
            {"code": "it", "name": "Italian"},
            {"code": "pt", "name": "Portuguese"},
            {"code": "ru", "name": "Russian"},
            {"code": "ja", "name": "Japanese"},
            {"code": "ko", "name": "Korean"},
            {"code": "zh", "name": "Chinese (Mandarin)"},
            {"code": "ar", "name": "Arabic"},
            {"code": "hi", "name": "Hindi"}
        ]
    }

if __name__ == "__main__":
    import uvicorn
    
    host = os.getenv("HOST", "0.0.0.0")
    port = int(os.getenv("PORT", 8000))
    
    # Disable reload in production (Railway)
    reload = os.getenv("ENVIRONMENT", "production").lower() == "development"
    
    uvicorn.run(
        "main:app",
        host=host,
        port=port,
        reload=reload,
        log_level="info"
    )
