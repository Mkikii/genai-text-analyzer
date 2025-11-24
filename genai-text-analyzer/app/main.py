from fastapi import FastAPI, HTTPException, Request
from pydantic import BaseModel
import os
import requests
import json
import logging
import datetime
import hashlib
import pickle
from dotenv import load_dotenv
from slowapi import Limiter, _rate_limit_exceeded_handler
from slowapi.util import get_remote_address
from slowapi.errors import RateLimitExceeded
import redis

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
    description="A production-ready microservice for text analysis using AI with Redis caching",
    version="1.0.0",
    docs_url="/"
)

app.state.limiter = limiter
app.add_exception_handler(RateLimitExceeded, _rate_limit_exceeded_handler)

# Redis configuration
REDIS_URL = os.getenv("REDIS_URL", "redis://localhost:6379")
try:
    redis_client = redis.Redis.from_url(REDIS_URL, decode_responses=False)
    # Test Redis connection
    redis_client.ping()
    logger.info("✅ Redis connected successfully")
except redis.ConnectionError as e:
    logger.error(f"❌ Redis connection failed: {e}")
    redis_client = None

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
    cached: bool = False

class HealthResponse(BaseModel):
    status: str
    message: str
    timestamp: str
    version: str
    redis_status: str

class CacheStatsResponse(BaseModel):
    total_requests: int
    cache_hits: int
    cache_misses: int
    hit_rate: float

# Cache statistics
cache_stats = {"hits": 0, "misses": 0}

def get_cache_key(text: str) -> str:
    """Generate cache key from text content"""
    return f"analysis:{hashlib.md5(text.encode()).hexdigest()}"

def get_cached_result(key: str):
    """Get result from Redis cache"""
    if not redis_client:
        return None
    
    try:
        cached = redis_client.get(key)
        if cached:
            cache_stats["hits"] += 1
            return pickle.loads(cached)
    except Exception as e:
        logger.warning(f"Cache read error: {e}")
    cache_stats["misses"] += 1
    return None

def set_cached_result(key: str, result: dict, expire: int = 3600):  # 1 hour expiration
    """Set result in Redis cache"""
    if not redis_client:
        return
    
    try:
        redis_client.setex(key, expire, pickle.dumps(result))
        logger.info(f"Cached result for key: {key}")
    except Exception as e:
        logger.warning(f"Cache write error: {e}")

@app.get("/health", response_model=HealthResponse)
@limiter.limit("30/minute")
async def health_check(request: Request):
    """Health check endpoint for deployment monitoring"""
    redis_status = "connected" if redis_client and redis_client.ping() else "disconnected"
    
    return HealthResponse(
        status="healthy",
        message="GenAI Text Analyzer API is running successfully!",
        timestamp=datetime.datetime.utcnow().isoformat(),
        version="1.0.0",
        redis_status=redis_status
    )

@app.get("/cache/stats", response_model=CacheStatsResponse)
@limiter.limit("30/minute")
async def get_cache_stats(request: Request):
    """Get cache statistics"""
    total = cache_stats["hits"] + cache_stats["misses"]
    hit_rate = cache_stats["hits"] / total if total > 0 else 0
    
    return CacheStatsResponse(
        total_requests=total,
        cache_hits=cache_stats["hits"],
        cache_misses=cache_stats["misses"],
        hit_rate=round(hit_rate, 2)
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

    # Check cache first
    cache_key = get_cache_key(text_request.text.strip())
    cached_result = get_cached_result(cache_key)
    
    if cached_result:
        logger.info(f"Cache hit for text analysis")
        return AnalysisResponse(**cached_result, cached=True)

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
        
        # Prepare response data
        result_data = {
            "sentiment": analysis_result.get("sentiment", "neutral"),
            "key_phrases": analysis_result.get("key_phrases", []),
            "summary": analysis_result.get("summary", ""),
            "confidence": analysis_result.get("confidence", 0.5),
            "model_used": "gpt-3.5-turbo",
            "cached": False
        }
        
        # Cache the result
        set_cached_result(cache_key, result_data)
        
        return AnalysisResponse(**result_data)

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

@app.delete("/cache/clear")
@limiter.limit("5/minute")
async def clear_cache(request: Request):
    """Clear all cached results"""
    if not redis_client:
        raise HTTPException(status_code=500, detail="Redis not available")
    
    try:
        # Clear all cache keys starting with "analysis:"
        keys = redis_client.keys("analysis:*")
        if keys:
            redis_client.delete(*keys)
        logger.info(f"Cleared {len(keys)} cached items")
        return {"message": f"Cleared {len(keys)} cached items"}
    except Exception as e:
        logger.error(f"Cache clear error: {e}")
        raise HTTPException(status_code=500, detail=f"Error clearing cache: {e}")

@app.get("/")
@limiter.limit("30/minute")
async def root(request: Request):
    """Root endpoint with API information"""
    redis_status = "connected" if redis_client and redis_client.ping() else "disconnected"
    
    return {
        "message": "GenAI Text Analyzer API with Redis Caching",
        "version": "1.0.0",
        "redis_status": redis_status,
        "endpoints": {
            "docs": "/docs",
            "health": "/health",
            "analyze": "/analyze",
            "cache_stats": "/cache/stats",
            "clear_cache": "/cache/clear"
        },
        "timestamp": datetime.datetime.utcnow().isoformat()
    }

if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app, host="0.0.0.0", port=8000)
