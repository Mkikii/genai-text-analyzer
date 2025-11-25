# Fix for cached response - remove the duplicate 'cached' parameter
@app.post("/analyze", response_model=AnalysisResponse)
@limiter.limit("10/minute")
async def analyze_text(request: Request, text_request: TextRequest):
    # ... existing validation code ...
    
    # Check cache first
    cache_key = get_cache_key(text_request.text.strip())
    cached_result = get_cached_result(cache_key)
    
    if cached_result:
        logger.info(f"Cache hit for text analysis")
        # Return the cached result directly (it already has cached=True)
        return AnalysisResponse(**cached_result)
    
    # ... rest of your existing analysis code ...
