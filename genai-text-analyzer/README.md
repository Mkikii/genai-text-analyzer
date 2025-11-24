# GenAI Text Analyzer Microservice

A production-ready FastAPI microservice for text analysis using Generative AI.

## Features

- **Sentiment Analysis**: Detect positive, negative, or neutral sentiment
- **Key Phrase Extraction**: Automatically identify important phrases
- **Text Summarization**: Generate concise summaries
- **RESTful API**: Fully documented with OpenAPI/Swagger
- **Dockerized**: Ready for deployment anywhere
- **Health Checks**: Production-ready monitoring

## Quick Start

### Prerequisites

- Docker and Docker Compose
- OpenAI API key

### 1. Clone and Setup

```bash
git clone <your-repo-url>
cd genai-text-analyzer

# Create .env file and add your API key
echo "OPENAI_API_KEY=your_actual_api_key_here" > .env
2. Run with Docker Compose
bash
docker-compose up --build
3. Access the API
API Documentation: http://localhost:8000

Health Check: http://localhost:8000/health

API Usage
Analyze Text
bash
curl -X POST "http://localhost:8000/analyze" \
     -H "Content-Type: application/json" \
     -d '{"text": "I absolutely love this new AI technology! It is transforming how we build applications."}'
Response
json
{
  "sentiment": "positive",
  "key_phrases": [
    "AI technology",
    "transforming applications",
    "developers productive"
  ],
  "summary": "The author expresses strong enthusiasm for new AI technology that is changing application development.",
  "confidence": 0.92,
  "model_used": "gpt-3.5-turbo"
}
Deployment
Deploy to Railway
Fork this repository

Go to Railway

Connect your GitHub repository

Add OPENAI_API_KEY environment variable

Deploy!

Deploy to Render
Fork this repository

Go to Render

Create a new Web Service

Connect your repository

Add OPENAI_API_KEY environment variable

Deploy!

Local Development
Without Docker
bash
# Create virtual environment
python -m venv venv
source venv/bin/activate  # On Windows: venv\Scripts\activate

# Install dependencies
pip install -r requirements.txt

# Set API key
export OPENAI_API_KEY=your_key_here

# Run server
uvicorn app:app --reload --host 0.0.0.0 --port 8000
Project Structure
text
genai-text-analyzer/
├── app.py               # FastAPI application
├── Dockerfile           # Container configuration
├── docker-compose.yml   # Local development
├── requirements.txt     # Python dependencies
├── .env.example         # Environment template
└── README.md           # This file
Environment Variables
OPENAI_API_KEY: Your OpenAI API key (required)

License
MIT

