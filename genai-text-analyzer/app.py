from fastapi import FastAPI, HTTPException, Request
from pydantic import BaseModel
import os
import requests
import json
import logging
from dotenv import load_dotenv
from slowapi import Limiter, _rate_limit_exceeded_handler
from slowapi.util import get_remote_address
from slowapi.errors import RateLimitExceeded
from slowapi.middleware import SlowAPIMiddleware

# Load environment variables from .env file
load_dotenv()

# Setup logging
logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s',
    handlers=[
        logging.StreamHandler(),
        logging.FileHandler('app.log')
    ]
)
logger = logging.getLogger(__name__)

# Rate limiter
limiter = Limiter(key_func=get_remote_address)

app = FastAPI(
    title="GenAI Text Analyzer API",
    description="A production-ready microservice for text analysis using AI",
    version="1.0.0",
    docs_url="/"
)

# Add rate limiting middleware
app.state.limiter = limiter
app.add_exception_handler(RateLimitExceeded, _rate_limit_exceeded_handler)
app.add_middleware(SlowAPIMiddleware)

# Get API key from environment variable
GENAI_API_KEY = os.getenv("OPENAI_API_KEY")
GENAI_URL = "https://api.openai.com/v1/chat/completions"

# Request and Response models
class TextRequest(BaseModel):
    text: str

class AnalysisResponse(BaseModel):
    sentiment: str
    key_phrases: list
    summary: str
    confidence: float
    model_used: str

class HealthResponse(BaseModel):
    status: str
    message: str
    timestamp: str
    version: str

@app.get("/health", response_model=HealthResponse)
@limiter.limit("30/minute")
async def health_check(request: Request):
    """Health check endpoint for deployment monitoring"""
    import datetime
    return HealthResponse(
        status="healthy",
        message="GenAI Text Analyzer API is running successfully!",
        timestamp=datetime.datetime.utcnow().isoformat(),
        version="1.0.0"
    )

@app.post("/analyze", response_model=AnalysisResponse)
@limiter.limit("10/minute")  # 10 requests per minute per IP
async def analyze_text(request: Request, text_request: TextRequest):
    """
    Analyze text for sentiment, key phrases, and generate a summary.
    
    - **text**: The input text to analyze (min 10 characters, max 1000 characters)
    """
    # Input validation
    if len(text_request.text.strip()) < 10:
        logger.warning(f"Text too short from IP: {request.client.host}")
        raise HTTPException(
            status_code=400, 
            detail="Text must be at least 10 characters long"
        )
    
    if len(text_request.text.strip()) > 1000:
        logger.warning(f"Text too long from IP: {request.client.host}")
        raise HTTPException(
            status_code=400, 
            detail="Text must be less than 1000 characters"
        )
    
    if not GENAI_API_KEY:
        logger.error("OpenAI API key not configured")
        raise HTTPException(
            status_code=500, 
            detail="API key not configured. Please set OPENAI_API_KEY in environment variables."
        )

    logger.info(f"Analyzing text from IP: {request.client.host}, length: {len(text_request.text)}")

    try:
        # Craft a detailed prompt for comprehensive analysis
        prompt = f"""
        Analyze the following text and provide a JSON response with exactly these fields:
        - "sentiment": one of "positive", "negative", or "neutral"
        - "key_phrases": array of exactly 3 most important phrases or keywords
        - "summary": a one-sentence summary of the text
        - "confidence": a number between 0 and 1 indicating analysis confidence

        Text: {text_request.text}

        Respond with valid JSON only, no other text.
        Example format:
        {{
            "sentiment": "positive",
            "key_phrases": ["phrase1", "phrase2", "phrase3"],
            "summary": "Brief summary here",
            "confidence": 0.95
        }}
        """

        headers = {
            "Authorization": f"Bearer {GENAI_API_KEY}",
            "Content-Type": "application/json"
        }
        
        data = {
            "model": "gpt-3.5-turbo",
            "messages": [{"role": "user", "content": prompt}],
            "temperature": 0.1,
            "max_tokens": 500
        }

        response = requests.post(GENAI_URL, json=data, headers=headers)
        response.raise_for_status()
        
        ai_content = response.json()['choices'][0]['message']['content'].strip()
        
        # Parse the JSON response from AI
        analysis_result = json.loads(ai_content)
        
        logger.info(f"Successfully analyzed text. Sentiment: {analysis_result.get('sentiment')}")
        
        return AnalysisResponse(
            sentiment=analysis_result.get("sentiment", "neutral"),
            key_phrases=analysis_result.get("key_phrases", []),
            summary=analysis_result.get("summary", ""),
            confidence=analysis_result.get("confidence", 0.5),
            model_used="gpt-3.5-turbo"
        )

    except requests.exceptions.RequestException as e:
        logger.error(f"OpenAI API error: {str(e)}")
        raise HTTPException(
            status_code=502,
            detail=f"Error calling AI service: {str(e)}"
        )
    except json.JSONDecodeError as e:
        logger.error(f"JSON parsing error: {str(e)}")
        raise HTTPException(
            status_code=500,
            detail=f"Error parsing AI response: {str(e)}"
        )
    except Exception as e:
        logger.error(f"Unexpected error: {str(e)}")
        raise HTTPException(
            status_code=500,
            detail=f"Unexpected error: {str(e)}"
        )

@app.get("/")
@limiter.limit("30/minute")
async def root(request: Request):
    """Root endpoint with API information"""
    return {
        "message": "GenAI Text Analyzer API",
        "version": "1.0.0",
        "endpoints": {
            "docs": "/docs",
            "health": "/health",
            "analyze": "/analyze"
        }
    }

if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app, host="0.0.0.0", port=8000)