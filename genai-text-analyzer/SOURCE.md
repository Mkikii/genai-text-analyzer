# 🧠 AI Prompt Journal - GenAI Text Analyzer

> Documentation of all AI prompts used during the development of this project

**Project**: GenAI Text Analyzer (FastAPI + OpenAI Integration)  
**Developer**: Maureen Karimi
**Course**: Moringa School AI Capstone Project  
**Date**: November 2025

---

## 📋 Table of Contents

1. [Learning Phase](#learning-phase)
2. [Setup & Configuration](#setup--configuration)
3. [Implementation Phase](#implementation-phase)
4. [Debugging & Troubleshooting](#debugging--troubleshooting)
5. [Documentation & Deployment](#documentation--deployment)
6. [Reflections & Learnings](#reflections--learnings)

---

## 🎓 Learning Phase

### Prompt 1: Understanding FastAPI

**Curriculum Link**: [FastAPI Introduction](https://ai.moringaschool.com)

**Prompt Used**:

```
Explain FastAPI framework and its advantages over Flask for building RESTful APIs.
Include specific use cases where FastAPI excels.
```

**AI Response Summary**:

- FastAPI is a modern Python web framework built on Starlette and Pydantic
- Key advantages: automatic API documentation, async support, data validation, type hints
- Excels in: High-performance APIs, microservices, ML model serving
- Better developer experience with auto-generated OpenAPI/Swagger docs

**My Evaluation**: ⭐⭐⭐⭐⭐ (5/5)

- Extremely helpful for understanding why to choose FastAPI
- Convinced me to use FastAPI over Flask for this project
- The comparison table was particularly useful

**Impact on Project**:
This prompt helped me decide the core technology for my capstone. I chose FastAPI because of its automatic documentation feature, which is perfect for a beginner's toolkit.

---

### Prompt 2: OpenAI API Integration Basics

**Curriculum Link**: [OpenAI API Fundamentals](https://ai.moringaschool.com)

**Prompt Used**:

```
How do I integrate OpenAI API with FastAPI for text analysis tasks?
Provide a basic example with sentiment analysis.
```

**AI Response Summary**:

- Install `openai` package via pip
- Use environment variables for API keys (security best practice)
- Create async functions for API calls to avoid blocking
- Structure: FastAPI endpoint → OpenAI API → Process response → Return JSON

**Sample Code Provided**:

```python
from openai import OpenAI
import os

client = OpenAI(api_key=os.getenv("OPENAI_API_KEY"))

async def analyze_sentiment(text: str):
    response = client.chat.completions.create(
        model="gpt-3.5-turbo",
        messages=[{"role": "user", "content": f"Analyze sentiment: {text}"}]
    )
    return response.choices[0].message.content
```

**My Evaluation**: ⭐⭐⭐⭐ (4/5)

- Very practical example
- Needed to refine for production use (error handling, retries)
- -1 star because it didn't include rate limiting discussion

**Impact on Project**:
This became the foundation of my `app.py`. I extended it to include key phrase extraction and summarization.

---

### Prompt 3: FastAPI Best Practices

**Curriculum Link**: [API Design Patterns](https://ai.moringaschool.com)

**Prompt Used**:

```
What are the best practices for structuring a production-ready FastAPI microservice?
Include folder structure, error handling, and health checks.
```

**AI Response Summary**:

- Use Pydantic models for request/response validation
- Implement health check endpoints (`/health`)
- Separate concerns: routers, models, services
- Use dependency injection for database connections
- Add CORS middleware for frontend integration
- Include proper error handling with HTTP status codes

**My Evaluation**: ⭐⭐⭐⭐⭐ (5/5)

- Comprehensive best practices guide
- Helped me structure the project professionally
- The health check endpoint recommendation was crucial for deployment

**Impact on Project**:
Implemented the `/health` endpoint and proper error handling based on this guidance. This made deployment to Railway much smoother.

---

## 🔧 Setup & Configuration

### Prompt 4: Docker Configuration

**Curriculum Link**: [Containerization Basics](https://ai.moringaschool.com)

**Prompt Used**:

```
Create a Dockerfile for a FastAPI application with OpenAI dependencies.
Include best practices for Python Docker images.
```

**AI Response Summary**:

```dockerfile
FROM python:3.9-slim
WORKDIR /app
COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt
COPY . .
EXPOSE 8000
CMD ["uvicorn", "app:app", "--host", "0.0.0.0", "--port", "8000"]
```

Recommendations:

- Use slim base images to reduce size
- Copy requirements first for better layer caching
- Use `--no-cache-dir` to reduce image size
- Expose port 8000 (FastAPI default)

**My Evaluation**: ⭐⭐⭐⭐⭐ (5/5)

- Production-ready Dockerfile
- Efficient layer caching strategy
- Used this exact structure in my project

**Impact on Project**:
This Dockerfile worked perfectly on first try! Deployed successfully to Railway and Render without modifications.

---

### Prompt 5: Docker Compose Setup

**Curriculum Link**: [Docker Compose Tutorial](https://ai.moringaschool.com)

**Prompt Used**:

```
How do I properly handle environment variables in Docker Compose with .env files
for an OpenAI API key? Show me a secure setup.
```

**AI Response Summary**:

```yaml
version: "3.8"
services:
  api:
    build: .
    ports:
      - "8000:8000"
    env_file:
      - .env
    environment:
      - OPENAI_API_KEY=${OPENAI_API_KEY}
```

Security tips:

- Never commit `.env` to Git
- Use `.env.example` template
- Mount `.env` file or use environment variables

**My Evaluation**: ⭐⭐⭐⭐ (4/5)

- Secure approach
- Needed to add `.gitignore` rules myself
- Works perfectly for local development

**Impact on Project**:
Implemented exactly as suggested. Added `.env.example` for other developers to use as a template.

---

## 💻 Implementation Phase

### Prompt 6: Sentiment Analysis Endpoint

**Curriculum Link**: [Building API Endpoints](https://ai.moringaschool.com)

**Prompt Used**:

```
Generate a FastAPI endpoint that accepts text input and returns sentiment analysis
using OpenAI. Include Pydantic models for request/response validation.
```

**AI Response Summary**:

```python
from fastapi import FastAPI
from pydantic import BaseModel

class TextRequest(BaseModel):
    text: str

class AnalysisResponse(BaseModel):
    sentiment: str
    confidence: float

@app.post("/analyze", response_model=AnalysisResponse)
async def analyze_text(request: TextRequest):
    # OpenAI API call here
    pass
```

**My Evaluation**: ⭐⭐⭐⭐⭐ (5/5)

- Perfect starting structure
- Pydantic validation prevents bad inputs
- Type hints make code maintainable

**Impact on Project**:
Extended this to include `key_phrases` and `summary` fields. The Pydantic models prevented several bugs during testing.

---

### Prompt 7: Multiple Analysis Features

**Curriculum Link**: [Advanced Prompt Engineering](https://ai.moringaschool.com)

**Prompt Used**:

```
Write an OpenAI prompt that performs sentiment analysis, key phrase extraction,
and summarization in a single API call. Return structured JSON.
```

**AI Response Summary**:

```python
prompt = f"""Analyze this text and return ONLY a JSON object with these fields:
- sentiment: "positive", "negative", or "neutral"
- key_phrases: array of 3-5 important phrases
- summary: one sentence summary
- confidence: 0-1 score

Text: {text}
"""
```

Tips:

- Be explicit about JSON format
- Request specific field names
- Include examples in prompt for consistency

**My Evaluation**: ⭐⭐⭐⭐⭐ (5/5)

- Brilliant approach to get structured output
- Single API call saves costs
- Consistent JSON format every time

**Impact on Project**:
This was a game-changer! Instead of 3 separate API calls, I get all analysis in one request. Reduced latency and costs significantly.

---

### Prompt 8: Health Check Implementation

**Curriculum Link**: [Production API Patterns](https://ai.moringaschool.com)

**Prompt Used**:

```
How do I implement health check endpoints in FastAPI for production monitoring?
Include timestamp and status checks.
```

**AI Response Summary**:

```python
from datetime import datetime

@app.get("/health")
async def health_check():
    return {
        "status": "healthy",
        "timestamp": datetime.utcnow().isoformat()
    }
```

Advanced version checks:

- Database connectivity
- External API availability
- Memory usage

**My Evaluation**: ⭐⭐⭐⭐ (4/5)

- Simple and effective
- Could include more detailed checks
- Perfect for basic deployment monitoring

**Impact on Project**:
Implemented the basic version. Railway and Render both use this endpoint to monitor service health automatically.

---

## 🐛 Debugging & Troubleshooting

### Prompt 9: CORS Configuration

**Curriculum Link**: [API Security Fundamentals](https://ai.moringaschool.com)

**Prompt Used**:

```
Why am I getting CORS errors in FastAPI and how do I fix them?
Show me the proper middleware configuration.
```

**AI Response Summary**:

```python
from fastapi.middleware.cors import CORSMiddleware

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],  # In production, specify domains
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)
```

**My Evaluation**: ⭐⭐⭐⭐ (4/5)

- Fixed the issue immediately
- Clear explanation of each parameter
- Security warning for production was helpful

**Impact on Project**:
Added this middleware to allow frontend testing. Will restrict origins before production deployment.

---

### Prompt 10: Error Handling for Rate Limits

**Curriculum Link**: [Robust API Design](https://ai.moringaschool.com)

**Prompt Used**:

```
Best way to structure error handling for OpenAI API rate limits in FastAPI.
Include retry logic with exponential backoff.
```

**AI Response Summary**:

```python
import time
from openai import RateLimitError

async def call_openai_with_retry(prompt, max_retries=3):
    for attempt in range(max_retries):
        try:
            response = await client.chat.completions.create(...)
            return response
        except RateLimitError:
            if attempt < max_retries - 1:
                wait_time = 2 ** attempt
                time.sleep(wait_time)
            else:
                raise
```

**My Evaluation**: ⭐⭐⭐⭐⭐ (5/5)

- Professional error handling
- Exponential backoff prevents API hammering
- Graceful failure after retries

**Impact on Project**:
Implemented this wrapper around all OpenAI calls. Significantly improved reliability during high-traffic testing.

---

### Prompt 11: Environment Variable Debugging

**Curriculum Link**: [Configuration Management](https://ai.moringaschool.com)

**Prompt Used**:

```
My Docker container can't read environment variables from .env file.
How do I debug and fix this issue?
```

**AI Response Summary**:
Common issues:

1. `.env` file not in same directory as `docker-compose.yml`
2. Syntax errors in `.env` file (no spaces around `=`)
3. Not rebuilding after changes

Debug steps:

```bash
# Check if env vars are loaded
docker-compose config

# Check inside container
docker exec <container> env | grep OPENAI
```

**My Evaluation**: ⭐⭐⭐⭐ (4/5)

- Systematic debugging approach
- Resolved my issue quickly
- Could include more edge cases

**Impact on Project**:
Found that I had a space in my `.env` file: `KEY = value` instead of `KEY=value`. Fixed immediately!

---

## 📚 Documentation & Deployment

### Prompt 12: API Documentation

**Curriculum Link**: [Technical Writing](https://ai.moringaschool.com)

**Prompt Used**:

```
Generate OpenAPI/Swagger documentation examples for a text analysis API.
Include request/response examples and error codes.
```

**AI Response Summary**:
FastAPI auto-generates docs at `/docs`, but can enhance with:

```python
@app.post(
    "/analyze",
    response_model=AnalysisResponse,
    summary="Analyze text with AI",
    description="Performs sentiment analysis, key phrase extraction, and summarization",
    responses={
        200: {"description": "Successful analysis"},
        400: {"description": "Invalid input"},
        500: {"description": "OpenAI API error"}
    }
)
```

**My Evaluation**: ⭐⭐⭐⭐⭐ (5/5)

- Makes API self-documenting
- Professional presentation
- Helps users understand errors

**Impact on Project**:
Added detailed docstrings to all endpoints. The Swagger UI at `/docs` now looks incredibly professional!

---

### Prompt 13: README Structure

**Curriculum Link**: [Open Source Best Practices](https://ai.moringaschool.com)

**Prompt Used**:

```
Create a professional README.md structure for a FastAPI GenAI project.
Include badges, quick start, and deployment instructions.
```

**AI Response Summary**:
Essential sections:

- Badges (tech stack, license)
- Quick start guide
- API usage examples
- Deployment instructions
- Common issues
- Contributing guidelines

**My Evaluation**: ⭐⭐⭐⭐⭐ (5/5)

- Comprehensive template
- GitHub-approved markdown
- Makes project look professional

**Impact on Project**:
Used this structure for my README. Added emojis and badges to make it visually appealing.

---

### Prompt 14: Deployment to Railway

**Curriculum Link**: [Cloud Deployment](https://ai.moringaschool.com)

**Prompt Used**:

```
Step-by-step guide to deploy a Dockerized FastAPI app to Railway.
Include environment variable configuration.
```

**AI Response Summary**:
Steps:

1. Push code to GitHub
2. Connect Railway to repository
3. Add `OPENAI_API_KEY` in Railway dashboard
4. Railway auto-detects Dockerfile
5. Deploy automatically

**My Evaluation**: ⭐⭐⭐⭐⭐ (5/5)

- Deployed successfully on first try
- Railway's auto-detection is amazing
- No configuration files needed

**Impact on Project**:
Deployed to Railway in under 5 minutes! Added deployment instructions to README for others to follow.

---

## 🎯 Reflections & Learnings

### Overall AI Assistance Impact

**Productivity Boost**: 🚀🚀🚀🚀🚀 (5/5)

- Reduced development time by ~60%
- Would have taken 2 weeks without AI, completed in 3 days
- Instant answers to documentation questions

**Learning Acceleration**: 📚📚📚📚📚 (5/5)

- Learned FastAPI fundamentals in hours instead of days
- Understood Docker best practices quickly
- Gained confidence to explore advanced features

**Code Quality**: ✨✨✨✨ (4/5)

- AI provided production-ready patterns
- Learned proper error handling
- Some generated code needed refinement for edge cases

---

### What Worked Best

1. **Specific, Context-Rich Prompts**

   - Instead of: "How to use FastAPI?"
   - Used: "Generate a FastAPI endpoint with Pydantic validation for text analysis"
   - Result: Immediately usable code

2. **Iterative Refinement**

   - Started with basic examples
   - Asked follow-up questions for edge cases
   - Built complexity incrementally

3. **Combining Multiple Sources**
   - Used AI for structure
   - Verified with official documentation
   - Tested in real environment

---

### What Could Be Improved

1. **AI Sometimes Over-Simplifies**

   - Production considerations not always included
   - Security best practices need explicit asking
   - Rate limiting and error handling require follow-up prompts

2. **Version Compatibility Issues**

   - AI suggested older OpenAI library syntax
   - Had to check official docs for latest API
   - Lesson: Always verify current versions

3. **Testing Strategies**
   - AI gave basic examples
   - Needed to research proper testing frameworks myself
   - Could have asked more specific testing prompts

---

### Key Takeaways

✅ **AI as Learning Partner**

- Best for getting unstuck quickly
- Excellent for explaining concepts
- Great for generating boilerplate code

✅ **Human Judgment Still Essential**

- Review and refine AI-generated code
- Consider security implications
- Test thoroughly in real conditions

✅ **Prompt Engineering is a Skill**

- Specific prompts → Better results
- Include context and constraints
- Ask for examples and edge cases

---

### Skills Developed

Through this AI-assisted learning journey, I developed:

1. **Technical Skills**

   - FastAPI framework proficiency
   - OpenAI API integration
   - Docker containerization
   - RESTful API design
   - Cloud deployment (Railway, Render)

2. **Soft Skills**

   - Prompt engineering techniques
   - Problem decomposition
   - Technical documentation writing
   - Debugging systematic approach

3. **Best Practices**
   - Environment variable management
   - Error handling patterns
   - API security fundamentals
   - Production deployment strategies

---

## 📊 Prompt Usage Statistics

| Phase          | Prompts Used | Time Saved    | Success Rate |
| -------------- | ------------ | ------------- | ------------ |
| Learning       | 3            | ~5 hours      | 100%         |
| Setup          | 2            | ~2 hours      | 100%         |
| Implementation | 3            | ~8 hours      | 100%         |
| Debugging      | 3            | ~4 hours      | 100%         |
| Documentation  | 3            | ~3 hours      | 100%         |
| **Total**      | **14**       | **~22 hours** | **100%**     |

---

## 🎓 Recommendations for Future Learners

### Do's ✅

- Start with broad learning prompts, then get specific
- Save and iterate on prompts that work well
- Cross-reference AI answers with official docs
- Test all generated code in your environment
- Document your prompt journey (like this file!)

### Don'ts ❌

- Don't blindly copy-paste without understanding
- Don't skip testing edge cases
- Don't ignore security warnings
- Don't assume AI knows latest library versions
- Don't forget to verify licensing and attributions

---

## 🌟 Conclusion

Using AI prompts for this capstone project was transformative. It allowed me to:

- Learn a new framework (FastAPI) rapidly
- Build a production-ready application
- Understand best practices without years of experience
- Deploy to cloud platforms confidently

**Most Valuable Lesson**: AI is an incredible learning accelerator, but the quality of output depends entirely on the quality of your prompts. Think of it as having an expert mentor available 24/7 - but you still need to ask the right questions!

---

**Project Repository**: [GenAI Text Analyzer](https://github.com/Mkikii/genai-text-analyzer)  
**Author**: Maureen Karimi  
**Course**: Moringa School AI Capstone  
**Submission Date**: November 26, 2024

---

_This document demonstrates how AI was used as a learning tool throughout the development process, fulfilling the "AI Prompt Journal" requirement of the capstone project._
