from fastapi import FastAPI, HTTPException, Request
from pydantic import BaseModel
import os
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

# Load environment variables
load_dotenv()

# Setup logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

# Rate limiter
limiter = Limiter(key_func=get_remote_address)

app = FastAPI(
    title="GenAI Text Analyzer API (Mock Mode)",
    description="Mock version for testing without real API keys",
    version="1.0.0",
    docs_url="/"
)

app.state.limiter = limiter
app.add_exception_handler(RateLimitExceeded, _rate_limit_exceeded_handler)

# Redis configuration
REDIS_URL = os.getenv("REDIS_URL", "redis://localhost:6379")
try:
    redis_client = redis.Redis.from_url(REDIS_URL, decode_responses=False)
    redis_client.ping()
    logger.info("✅ Redis connected successfully")
except redis.ConnectionError:
    logger.error("❌ Redis connection failed")
    redis_client = None

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
    return f"analysis:{hashlib.md5(text.encode()).hexdigest()}"

def get_cached_result(key: str):
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

def set_cached_result(key: str, result: dict, expire: int = 3600):
    if not redis_client:
        return
    try:
        redis_client.setex(key, expire, pickle.dumps(result))
    except Exception as e:
        logger.warning(f"Cache write error: {e}")

def mock_ai_analysis(text: str) -> dict:
    """Mock AI analysis that simulates OpenAI responses"""
    # Simple sentiment analysis based on keywords
    text_lower = text.lower()
    
    if any(word in text_lower for word in ['love', 'amazing', 'great', 'excellent', 'awesome']):
        sentiment = "positive"
        confidence = 0.9
    elif any(word in text_lower for word in ['hate', 'terrible', 'awful', 'bad', 'disappointing']):
        sentiment = "negative" 
        confidence = 0.8
    else:
        sentiment = "neutral"
        confidence = 0.7
    
    # Generate mock key phrases (first 3 words)
    words = [w for w in text.split() if len(w) > 3][:3]
    key_phrases = words if words else ["sample", "test", "phrases"]
    
    # Generate mock summary
    summary = f"This text expresses {sentiment} sentiment about {key_phrases[0] if key_phrases else 'the topic'}."
    
    return {
        "sentiment": sentiment,
        "key_phrases": key_phrases,
        "summary": summary,
        "confidence": confidence
    }

@app.get("/health", response_model=HealthResponse)
@limiter.limit("30/minute")
async def health_check(request: Request):
    redis_status = "connected" if redis_client and redis_client.ping() else "disconnected"
    return HealthResponse(
        status="healthy",
        message="GenAI Text Analyzer API (Mock Mode) is running successfully!",
        timestamp=datetime.datetime.utcnow().isoformat(),
        version="1.0.0",
        redis_status=redis_status
    )

@app.get("/cache/stats", response_model=CacheStatsResponse)
@limiter.limit("30/minute")
async def get_cache_stats(request: Request):
    total = cache_stats["hits"] + cache_stats["misses"]
    hit_rate = cache_stats["hits"] / total if total > 0 else 0
    return CacheStatsResponse(
        total_requests=total,
        cache_hits=cache_stats["hits"],
        cache_misses=cache_stats["misses"],
        hit_rate=round(hit_rate, 2)
    )

@app.post("/analyze", response_model=AnalysisResponse)
@limiter.limit("10/minute")
async def analyze_text(request: Request, text_request: TextRequest):
    # Input validation
    if len(text_request.text.strip()) < 10:
        raise HTTPException(status_code=400, detail="Text must be at least 10 characters long")
    
    if len(text_request.text.strip()) > 1000:
        raise HTTPException(status_code=400, detail="Text must be less than 1000 characters")

    logger.info(f"Analyzing text (mock mode): {text_request.text[:50]}...")

    # Check cache first
    cache_key = get_cache_key(text_request.text.strip())
    cached_result = get_cached_result(cache_key)
    
    if cached_result:
        logger.info("Cache hit for text analysis")
        return AnalysisResponse(**cached_result, cached=True)

    # Use mock AI analysis
    analysis_result = mock_ai_analysis(text_request.text.strip())
    
    logger.info(f"Mock analysis complete. Sentiment: {analysis_result['sentiment']}")
    
    # Prepare response data
    result_data = {
        "sentiment": analysis_result["sentiment"],
        "key_phrases": analysis_result["key_phrases"],
        "summary": analysis_result["summary"],
        "confidence": analysis_result["confidence"],
        "model_used": "mock-gpt-3.5-turbo",
        "cached": False
    }
    
    # Cache the result
    set_cached_result(cache_key, result_data)
    
    return AnalysisResponse(**result_data)

@app.delete("/cache/clear")
@limiter.limit("5/minute")
async def clear_cache(request: Request):
    if not redis_client:
        raise HTTPException(status_code=500, detail="Redis not available")
    try:
        keys = redis_client.keys("analysis:*")
        if keys:
            redis_client.delete(*keys)
        return {"message": f"Cleared {len(keys)} cached items"}
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Error clearing cache: {e}")

if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app, host="0.0.0.0", port=8000)
