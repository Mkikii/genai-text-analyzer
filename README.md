# 🤖 GenAI Text Analyzer



 A production-ready FastAPI microservice for intelligent text analysis using Generative AI

[![FastAPI](https://img.shields.io/badge/FastAPI-0.104.1-009688?style=flat&logo=fastapi)](https://fastapi.tiangolo.com/)
[![OpenAI](https://img.shields.io/badge/OpenAI-API-412991?style=flat&logo=openai)](https://openai.com/)
[![Docker](https://img.shields.io/badge/Docker-Ready-2496ED?style=flat&logo=docker)](https://www.docker.com/)
[![Python](https://img.shields.io/badge/Python-3.9+-3776AB?style=flat&logo=python)](https://python.org)
[![License: MIT](https://img.shields.io/badge/License-MIT-yellow.svg)](LICENSE)

## 🌟 Live Deployment

- **🌐 Live API**: https://genai-text-analyzer.onrender.com
- **📚 API Documentation**: https://genai-text-analyzer.onrender.com/docs
- **🐙 GitHub Repository**: https://github.com/Mkikii/genai-text-analyzer

## 📋 Table of Contents

- [Overview](#-overview)
- [Features](#-features)
- [Technology Stack](#-technology-stack)
- [Quick Start](#-quick-start)
- [API Documentation](#-api-documentation)
- [Project Structure](#-project-structure)
- [Deployment](#-deployment)
- [Development](#-development)
- [Testing](#-testing)
- [Troubleshooting](#-troubleshooting)
- [Contributing](#-contributing)
- [License](#-license)

## 🎯 Overview

**GenAI Text Analyzer** is a FastAPI microservice that leverages OpenAI's GPT models to provide intelligent text analysis capabilities. Built as part of the Moringa AI Capstone, this project demonstrates modern API development with GenAI integration.

### Key Capabilities

- 📊 **Sentiment Analysis** - Detect emotional tone in text
- 🔑 **Key Phrase Extraction** - Identify important topics and concepts
- 📝 **Text Summarization** - Generate concise summaries
- 🎯 **Confidence Scoring** - Reliability metrics for analysis
- ⚡ **Redis Caching** - Intelligent response caching for performance
- 🛡️ **Rate Limiting** - API protection with configurable limits

## ✨ Features

| Feature | Status | Description |
|---------|--------|-------------|
| Sentiment Analysis | ✅ Live | Positive/Negative/Neutral classification |
| Key Phrase Extraction | ✅ Live | Automatic topic identification |
| Text Summarization | ✅ Live | Concise summary generation |
| RESTful API | ✅ Live | Fully documented OpenAPI/Swagger |
| Docker Support | ✅ Live | Containerized deployment |
| Health Monitoring | ✅ Live | Production-ready health checks |
| Redis Caching | ✅ Live | Intelligent response caching |
| Rate Limiting | ✅ Live | API protection layer |

## 🛠️ Technology Stack

**Backend Framework**
- **FastAPI** - Modern Python web framework with automatic API docs
- **Uvicorn** - ASGI server for high performance
- **Pydantic** - Data validation and settings management

**AI & Machine Learning**
- **OpenAI GPT-3.5/4** - Generative AI for text analysis
- **OpenAI API** - RESTful API integration

**Infrastructure**
- **Docker** - Containerization and deployment
- **Docker Compose** - Multi-container orchestration
- **Redis** - Response caching and performance
- **Render** - Cloud deployment platform

**Language**
- **Python 3.9+** - Primary programming language

## 🚀 Quick Start

### Prerequisites

- **Docker** & **Docker Compose**
- **OpenAI API Key** ([Get one here](https://platform.openai.com/api-keys))

### Option 1: Docker Compose (Recommended)


# 1. Clone the repository
git clone https://github.com/Mkikii/genai-text-analyzer.git
cd genai-text-analyzer

# 2. Create environment file
cp .env.example .env
# Edit .env and add your OpenAI API key:
# OPENAI_API_KEY=sk-your-actual-key-here

# 3. Build and launch
docker-compose up --build

# 4. Access the application
# API Documentation: http://localhost:8000/docs
# Health Check: http://localhost:8000/health

Option 2: Local Development
# 1. Clone and setup
git clone https://github.com/Mkikii/genai-text-analyzer.git
cd genai-text-analyzer

# 2. Create virtual environment
python -m venv venv
source venv/bin/activate  # Linux/macOS
# venv\Scripts\activate  # Windows

# 3. Install dependencies
pip install -r requirements.txt

# 4. Set environment variables
export OPENAI_API_KEY=your_key_here  # Linux/macOS
# set OPENAI_API_KEY=your_key_here  # Windows

# 5. Run the application
uvicorn app.main:app --reload --host 0.0.0.0 --port 8000
📡 API Documentation
Interactive Docs
Production: https://genai-text-analyzer.onrender.com/docs

Local: http://localhost:8000/docs

API Endpoints
Method	Endpoint	Description
GET	/health	Service health status
POST	/analyze	Analyze text with AI
GET	/cache/stats	Redis cache statistics
DELETE	/cache/clear	Clear cache
GET	/docs	Interactive API documentation
Analyze Text
Endpoint: POST /analyze

Request:

curl -X POST "https://genai-text-analyzer.onrender.com/analyze" \
  -H "Content-Type: application/json" \
  -d '{
    "text": "I absolutely love this new AI technology! It is transforming how we build applications and making developers more productive."
  }'
  Response:
  {
  "analysis": {
    "sentiment": "positive",
    "key_phrases": [
      "AI technology",
      "transforming applications", 
      "developers productive"
    ],
    "summary": "The author expresses strong enthusiasm for new AI technology that is changing application development and improving developer productivity.",
    "confidence": 0.92
  },
  "model_used": "gpt-3.5-turbo",
  "cached": false
}
Health Check
Endpoint: GET /health

Response:
{
  "status": "healthy",
  "timestamp": "2024-01-20T10:30:00Z",
  "version": "1.0.0"
}
Cache Statistics
Endpoint: GET /cache/stats

Response:
{
  "hits": 45,
  "misses": 12,
  "hit_rate": 0.79,
  "total_requests": 57
}
{
  "hits": 45,
  "misses": 12,
  "hit_rate": 0.79,
  "total_requests": 57
}
📁 Project Structure
genai-text-analyzer/
├── app/
│   ├── main.py              # FastAPI application entry point
│   ├── models.py            # Pydantic models for request/response
│   ├── services.py          # OpenAI integration service
│   └── cache.py             # Redis caching layer
├── tests/                   # Test suite
├── SOURCE.md                #AI learning journal and prompts
├── Dockerfile              # Container configuration
├── docker-compose.yml      # Multi-service orchestration
├── requirements.txt        # Python dependencies
├── .env.example           # Environment variables template
├── .gitignore            # Git ignore rules
└── README.md             # Project documentation

🌐 Deployment
Render (Production)
# Auto-deploys from main branch
# Live at: https://genai-text-analyzer.onrender.com
Railway Deployment
Fork this repository

Go to Railway

Create New Project → Connect GitHub repository

Add environment variable: OPENAI_API_KEY

Deploy - Railway auto-detects the Dockerfile

Render Deployment
Fork this repository

Go to Render

Create New Web Service

Connect your GitHub repository

Add environment variable: OPENAI_API_KEY

Deploy the service

🛠️ Development
Running Tests
# Run the test suite
pytest tests/ -v

# Run with coverage report
pytest --cov=app tests/

# Run specific test file
pytest tests/test_api.py -v
Code Quality
# Format code
black app/ tests/

# Lint code
flake8 app/ tests/

# Type checking
mypy app/

Building for Production
# Build Docker image
docker build -t genai-text-analyzer .

# Run production container
docker run -p 8000:8000 -e OPENAI_API_KEY=your_key_here genai-text-analyzer
⚙️ Configuration
Environment Variables:
OPENAI_API_KEY=your_openai_key_here
REDIS_URL=redis://localhost:6379
RATE_LIMIT=100/DAY
🧪 Testing
# Run all tests
pytest tests/ -v

# Run with coverage report
pytest --cov=app --cov-report=html tests/

# View detailed coverage in browser
open htmlcov/index.html
Test Coverage: 39% (focused on core API functionality)
Tests Passing: 13/13 ✅

## 🧪 Testing


# Run all tests
pytest tests/ -v

# Run with coverage report
pytest --cov=app --cov-report=html tests/

# View detailed coverage in browser
open htmlcov/index.html

⚠️ Troubleshooting
Common Issues
Port 6379 Already in Use
# Stop existing Redis service
sudo systemctl stop redis-server

# Or change Redis port in docker-compose.yml
services:
  redis:
    ports:
      - "6380:6379"  # Use different host port
      OpenAI API Key Issues
      # Verify environment variable is set
echo $OPENAI_API_KEY

# For Docker, ensure .env file exists
docker-compose down
docker-compose up --build
Docker Build Failures
Rate Limit Exceeded

Wait 1 minute and retry

Implement exponential backoff in your client

Consider upgrading OpenAI plan

🤝 Contributing
We welcome contributions! Please see our Contributing Guide for details.

Development Workflow
Fork the repository

Create a feature branch (git checkout -b feature/amazing-feature)

Commit changes (git commit -m 'Add amazing feature')

Push to branch (git push origin feature/amazing-feature)

Open a Pull Request

Code Standards
Follow PEP 8 style guide

Include type hints for new functions

Add tests for new features

Update documentation accordingly

📄 License
This project is licensed under the MIT License - see the LICENSE file for details.

👨‍💻 Author
Maureen Karimi

GitHub: @Mkikii

Project: GenAI Text Analyzer

🙏 Acknowledgments
Moringa School - AI Capstone Project framework

OpenAI - GPT models and API infrastructure

FastAPI - Excellent documentation and community

Render - Deployment platform
