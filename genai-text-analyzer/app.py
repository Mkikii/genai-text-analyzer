from fastapi import FastAPI, HTTPException
from pydantic import BaseModel
import os
import requests
from dotenv import load_dotenv

# Load environment variables from .env file
load_dotenv()

app = FastAPI(
    title="GenAI Text Analyzer API",
    description="A production-ready microservice for text analysis using AI",
    version="1.0.0",
    docs_url="/"
)

# Get API key from environment variable
GENAI_API_KEY = os.getenv("GENAI_API_KEY")
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

@app.get("/health", response_model=HealthResponse)
async def health_check():
    """Health check endpoint for deployment monitoring"""
    return HealthResponse(
        status="healthy",
        message="GenAI Text Analyzer API is running successfully!"
    )

@app.post("/analyze", response_model=AnalysisResponse)
async def analyze_text(request: TextRequest):
    """
    Analyze text for sentiment, key phrases, and generate a summary.
    
    - **text**: The input text to analyze (min 10 characters)
    """
    # Input validation
    if len(request.text.strip()) < 10:
        raise HTTPException(
            status_code=400, 
            detail="Text must be at least 10 characters long"
        )
    
    if not GENAI_API_KEY:
        raise HTTPException(
            status_code=500, 
            detail="API key not configured. Please set OPENAI_API_KEY in environment variables."
        )

    try:
        # Craft a detailed prompt for comprehensive analysis
        prompt = f"""
        Analyze the following text and provide a JSON response with exactly these fields:
        - "sentiment": one of "positive", "negative", or "neutral"
        - "key_phrases": array of exactly 3 most important phrases or keywords
        - "summary": a one-sentence summary of the text
        - "confidence": a number between 0 and 1 indicating analysis confidence

        Text: {request.text}

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

        response = requests.post(GENAI_API_URL, json=data, headers=headers)
        response.raise_for_status()
        
        ai_content = response.json()['choices'][0]['message']['content'].strip()
        
        # Parse the JSON response from AI
        import json
        analysis_result = json.loads(ai_content)
        
        return AnalysisResponse(
            sentiment=analysis_result.get("sentiment", "neutral"),
            key_phrases=analysis_result.get("key_phrases", []),
            summary=analysis_result.get("summary", ""),
            confidence=analysis_result.get("confidence", 0.5),
            model_used="gpt-3.5-turbo"
        )

    except requests.exceptions.RequestException as e:
        raise HTTPException(
            status_code=502,
            detail=f"Error calling AI service: {str(e)}"
        )
    except json.JSONDecodeError as e:
        raise HTTPException(
            status_code=500,
            detail=f"Error parsing AI response: {str(e)}"
        )
    except Exception as e:
        raise HTTPException(
            status_code=500,
            detail=f"Unexpected error: {str(e)}"
        )

if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app, host="0.0.0.0", port=8000)