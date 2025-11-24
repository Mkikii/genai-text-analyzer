from fastapi import FastAPI
from pydantic import BaseModel
import datetime

app = FastAPI(title="GenAI Text Analyzer - Mock API")

class AnalysisResponse(BaseModel):
    sentiment: str
    key_phrases: list
    summary: str
    confidence: float
    model_used: str
    cached: bool = False

class TextRequest(BaseModel):
    text: str

@app.post("/analyze", response_model=AnalysisResponse)
async def analyze_text_mock(request: TextRequest):
    """Mock analyze endpoint for testing without OpenAI"""
    return AnalysisResponse(
        sentiment="positive",
        key_phrases=["mock testing", "API working", "no OpenAI needed"],
        summary="This is a mock response showing the API structure works",
        confidence=0.95,
        model_used="mock-gpt-3.5-turbo",
        cached=False
    )

@app.get("/health")
async def health_check():
    return {"status": "healthy", "message": "Mock API running"}

if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app, host="0.0.0.0", port=8001)
