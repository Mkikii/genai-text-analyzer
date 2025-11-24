# Add to imports at top
import redis
import hashlib
import pickle

# Add after environment variables
# Redis cache setup
redis_client = redis.Redis(host='redis', port=6379, decode_responses=False)

def get_cache_key(text: str) -> str:
    """Generate cache key from text"""
    return hashlib.md5(text.encode()).hexdigest()

def get_cached_result(key: str):
    """Get result from cache"""
    try:
        cached = redis_client.get(key)
        if cached:
            return pickle.loads(cached)
    except Exception as e:
        logger.warning(f"Cache read error: {e}")
    return None

def set_cached_result(key: str, result: dict, expire: int = 3600):  # 1 hour
    """Set result in cache"""
    try:
        redis_client.setex(key, expire, pickle.dumps(result))
    except Exception as e:
        logger.warning(f"Cache write error: {e}")

# Modify the analyze_text function to include caching
@app.post("/analyze", response_model=AnalysisResponse)
@limiter.limit("10/minute")
async def analyze_text(request: Request, text_request: TextRequest):
    # ... existing validation code ...
    
    # Check cache first
    cache_key = get_cache_key(text_request.text.strip())
    cached_result = get_cached_result(cache_key)
    
    if cached_result:
        logger.info(f"Cache hit for text analysis")
        return AnalysisResponse(**cached_result)
    
    # ... existing analysis code ...
    
    # After successful analysis, cache the result
    result_data = {
        "sentiment": analysis_result.get("sentiment", "neutral"),
        "key_phrases": analysis_result.get("key_phrases", []),
        "summary": analysis_result.get("summary", ""),
        "confidence": analysis_result.get("confidence", 0.5),
        "model_used": "gpt-3.5-turbo"
    }
    
    set_cached_result(cache_key, result_data)
    
    return AnalysisResponse(**result_data)