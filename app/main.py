from fastapi import FastAPI, HTTPException, Request
from pydantic import BaseModel, ConfigDict
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

# Redis configuration - try multiple connection options
redis_client = None
redis_connection_attempts = [
    "redis://localhost:6379",  # Local Redis
    "redis://redis:6379",      # Docker Redis
    "redis://127.0.0.1:6379"   # Local IP
]

for redis_url in redis_connection_attempts:
    try:
        redis_client = redis.Redis.from_url(redis_url, decode_responses=False, socket_connect_timeout=2)
        redis_client.ping()
        logger.info(f"✅ Redis connected successfully to: {redis_url}")
        break
    except (redis.ConnectionError, redis.TimeoutError) as e:
        logger.warning(f"❌ Redis connection failed to {redis_url}: {e}")
        redis_client = None
        continue

if not redis_client:
    logger.warning("❌ All Redis connection attempts failed. Running without Redis caching.")

# Get API key from environment variable
GENAI_API_KEY = os.getenv("OPENAI_API_KEY")
GENAI_URL = "https://api.openai.com/v1/chat/completions"

# Request and Response models
class TextRequest(BaseModel):
    model_config = ConfigDict(protected_namespaces=())
    text: str

class AnalysisResponse(BaseModel):
    model_config = ConfigDict(protected_namespaces=())
    sentiment: str
    key_phrases: list
    summary: str
    confidence: float
    model_used: str
    cached: bool = False

class HealthResponse(BaseModel):
    model_config = ConfigDict(protected_namespaces=())
    status: str
    message: str
    timestamp: str
    version: str
    redis_status: str

class CacheStatsResponse(BaseModel):
    model_config = ConfigDict(protected_namespaces=())
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
            result = pickle.loads(cached)
            # Set cached to True when retrieving from cache
            result["cached"] = True
            return result
    except Exception as e:
        logger.warning(f"Cache read error: {e}")
    cache_stats["misses"] += 1
    return None

def set_cached_result(key: str, result: dict):
    """Set result in Redis cache"""
    if not redis_client:
        return
    
    try:
        # Store with cached=False for new results
        result_to_store = result.copy()
        result_to_store["cached"] = False
        redis_client.set(key, pickle.dumps(result_to_store))
        logger.info(f"Cached result for key: {key}")
    except Exception as e:
        logger.warning(f"Cache write error: {e}")

def mock_ai_analysis(text: str) -> dict:
    """Mock AI analysis that simulates OpenAI responses without API calls"""
    text_lower = text.lower()
    
    # Simple sentiment analysis based on keywords
    positive_words = ['love', 'amazing', 'great', 'excellent', 'awesome', 'wonderful', 'fantastic', 'perfect', 'good', 'best']
    negative_words = ['hate', 'terrible', 'awful', 'bad', 'disappointing', 'worst', 'horrible', 'dislike', 'annoying']
    
    positive_count = sum(1 for word in positive_words if word in text_lower)
    negative_count = sum(1 for word in negative_words if word in text_lower)
    
    if positive_count > negative_count:
        sentiment = "positive"
        confidence = min(0.9, 0.7 + (positive_count * 0.05))
    elif negative_count > positive_count:
        sentiment = "negative"
        confidence = min(0.9, 0.7 + (negative_count * 0.05))
    else:
        sentiment = "neutral"
        confidence = 0.7
    
    # Generate mock key phrases (most frequent words excluding common words)
    common_words = {'the', 'a', 'an', 'and', 'or', 'but', 'in', 'on', 'at', 'to', 'for', 'of', 'with', 'by'}
    words = [word.lower() for word in text.split() if len(word) > 3 and word.lower() not in common_words]
    
    # Get top 3 unique words as key phrases
    from collections import Counter
    word_freq = Counter(words)
    key_phrases = [word for word, _ in word_freq.most_common(3)]
    
    # If not enough unique words, add some defaults
    while len(key_phrases) < 3:
        key_phrases.append(f"topic{len(key_phrases) + 1}")
    
    # Generate mock summary based on sentiment and key phrases
    if sentiment == "positive":
        summary = f"This text expresses positive sentiment about {', '.join(key_phrases[:2])} with enthusiasm."
    elif sentiment == "negative":
        summary = f"This text expresses negative views regarding {', '.join(key_phrases[:2])} with criticism."
    else:
        summary = f"This text discusses {', '.join(key_phrases[:2])} in a neutral manner."
    
    return {
        "sentiment": sentiment,
        "key_phrases": key_phrases[:3],
        "summary": summary,
        "confidence": round(confidence, 2)
    }

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

    logger.info(f"Analyzing text from IP: {request.client.host}, length: {len(text_request.text)}")

    # Check cache first
    cache_key = get_cache_key(text_request.text.strip())
    cached_result = get_cached_result(cache_key)
    
    if cached_result:
        logger.info(f"Cache hit for text analysis")
        return AnalysisResponse(**cached_result)

    # Use mock analysis if no API key, otherwise use real OpenAI
    if not GENAI_API_KEY:
        logger.info("No API key found, using mock analysis")
        analysis_result = mock_ai_analysis(text_request.text.strip())
        model_used = "mock-gpt-3.5-turbo"
    else:
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
            model_used = "gpt-3.5-turbo"
            
        except requests.exceptions.RequestException as e:
            logger.error(f"OpenAI API error: {str(e)}, falling back to mock analysis")
            analysis_result = mock_ai_analysis(text_request.text.strip())
            model_used = "mock-gpt-3.5-turbo (fallback)"
        except json.JSONDecodeError as e:
            logger.error(f"JSON parsing error: {str(e)}, falling back to mock analysis")
            analysis_result = mock_ai_analysis(text_request.text.strip())
            model_used = "mock-gpt-3.5-turbo (fallback)"
        except Exception as e:
            logger.error(f"Unexpected error: {str(e)}, falling back to mock analysis")
            analysis_result = mock_ai_analysis(text_request.text.strip())
            model_used = "mock-gpt-3.5-turbo (fallback)"

    logger.info(f"Successfully analyzed text. Sentiment: {analysis_result.get('sentiment')}")
    
    # Prepare response data
    result_data = {
        "sentiment": analysis_result.get("sentiment", "neutral"),
        "key_phrases": analysis_result.get("key_phrases", []),
        "summary": analysis_result.get("summary", ""),
        "confidence": analysis_result.get("confidence", 0.5),
        "model_used": model_used,
        "cached": False
    }
    
    # Cache the result (no expiration)
    set_cached_result(cache_key, result_data)
    
    return AnalysisResponse(**result_data)

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
    api_mode = "Mock Mode" if not GENAI_API_KEY else "OpenAI Mode"
    
    return {
        "message": f"GenAI Text Analyzer API with Redis Caching ({api_mode})",
        "version": "1.0.0",
        "redis_status": redis_status,
        "api_mode": api_mode,
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