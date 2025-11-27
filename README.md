# GenAI Text Analyzer 🤖

[![FastAPI](https://img.shields.io/badge/FastAPI-005571?style=for-the-badge&logo=fastapi)](https://fastapi.tiangolo.com/)
[![OpenAI](https://img.shields.io/badge/OpenAI-412991?style=for-the-badge&logo=openai&logoColor=white)](https://openai.com/)
[![Docker](https://img.shields.io/badge/Docker-2496ED?style=for-the-badge&logo=docker&logoColor=white)](https://www.docker.com/)
[![Python](https://img.shields.io/badge/Python-3776AB?style=for-the-badge&logo=python&logoColor=white)](https://www.python.org/)

A production-ready FastAPI microservice that leverages OpenAI's Generative AI for intelligent text analysis. Built as part of Moringa School's AI Capstone Project.

## ✨ Features

- **Sentiment Analysis** - Detect positive, negative, or neutral sentiment in text
- **Key Phrase Extraction** - Automatically identify the most important phrases
- **Text Summarization** - Generate concise, accurate summaries
- **RESTful API** - Fully documented with OpenAPI/Swagger
- **Production Ready** - Dockerized with health checks and monitoring
- **Easy Deployment** - Deploy to Railway, Render, or any cloud platform

## 📋 Prerequisites

- Docker and Docker Compose installed
- OpenAI API key ([Get one here](https://platform.openai.com/api-keys))

## 🚀 Quick Start

### 1. Clone the Repository

```bash
git clone https://github.com/Mkikii/genai-text-analyzer.git
cd genai-text-analyzer
git checkout dev
```

### 2. Set Up Environment Variables

Create a `.env` file in the project root:

```bash
echo "OPENAI_API_KEY=your_actual_api_key_here" > .env
```

### 3. Run with Docker Compose

```bash
docker-compose up --build
```

The API will be available at:
- **API Documentation**: http://localhost:8000/docs
- **Health Check**: http://localhost:8000/health
- **Alternative Docs**: http://localhost:8000/redoc

## 📖 API Usage

### Analyze Text Endpoint

**POST** `/analyze`

#### Request

```bash
curl -X POST "http://localhost:8000/analyze" \
  -H "Content-Type: application/json" \
  -d '{
    "text": "I absolutely love this new AI technology! It is transforming how we build applications and making developers more productive."
  }'
```

#### Response

```json
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
```

### Health Check Endpoint

**GET** `/health`

```bash
curl http://localhost:8000/health
```

Response:
```json
{
  "status": "healthy",
  "timestamp": "2024-01-15T10:30:00Z"
}
```

## 🏗️ Project Structure

```
genai-text-analyzer/
├── app.py                 # FastAPI application with endpoints
├── Dockerfile            # Container configuration
├── docker-compose.yml    # Local development setup
├── requirements.txt      # Python dependencies
├── .env.example         # Environment variables template
├── .env                 # Your API keys (do not commit!)
└── README.md           # This file
```

## 🛠️ Local Development (Without Docker)

### 1. Create Virtual Environment

```bash
python -m venv venv

# On Windows
venv\Scripts\activate

# On macOS/Linux
source venv/bin/activate
```

### 2. Install Dependencies

```bash
pip install -r requirements.txt
```

### 3. Set Environment Variable

```bash
# On Windows (CMD)
set OPENAI_API_KEY=your_key_here

# On Windows (PowerShell)
$env:OPENAI_API_KEY="your_key_here"

# On macOS/Linux
export OPENAI_API_KEY=your_key_here
```

### 4. Run the Server

```bash
uvicorn app:app --reload --host 0.0.0.0 --port 8000
```

## ☁️ Deployment Options

### Deploy to Railway

1. Fork this repository
2. Go to [Railway](https://railway.app/)
3. Click "New Project" → "Deploy from GitHub"
4. Select your forked repository
5. Add environment variable: `OPENAI_API_KEY`
6. Deploy!

### Deploy to Render

1. Fork this repository
2. Go to [Render](https://render.com/)
3. Click "New" → "Web Service"
4. Connect your GitHub repository
5. Add environment variable: `OPENAI_API_KEY`
6. Deploy!

## 🧪 Testing the API

### Using Python Requests

```python
import requests

url = "http://localhost:8000/analyze"
data = {
    "text": "FastAPI is an amazing framework for building APIs quickly!"
}

response = requests.post(url, json=data)
print(response.json())
```

### Using JavaScript Fetch

```javascript
fetch('http://localhost:8000/analyze', {
  method: 'POST',
  headers: {
    'Content-Type': 'application/json',
  },
  body: JSON.stringify({
    text: 'This API makes text analysis so easy!'
  })
})
.then(response => response.json())
.then(data => console.log(data));
```

## 📊 Example Use Cases

1. **Customer Feedback Analysis** - Analyze customer reviews to understand sentiment
2. **Social Media Monitoring** - Track brand sentiment across social platforms
3. **Content Summarization** - Generate summaries for long articles or documents
4. **Email Triage** - Automatically categorize and prioritize emails
5. **Market Research** - Extract key insights from survey responses

## 🔧 Configuration

### Environment Variables

| Variable | Description | Required |
|----------|-------------|----------|
| `OPENAI_API_KEY` | Your OpenAI API key | Yes |

### API Parameters

The `/analyze` endpoint accepts:
- **text** (string, required): The text to analyze (max 4000 characters)

## 📚 Technologies Used

- **[FastAPI](https://fastapi.tiangolo.com/)** - Modern, fast web framework for building APIs
- **[OpenAI GPT-3.5 Turbo](https://platform.openai.com/)** - State-of-the-art language model
- **[Docker](https://www.docker.com/)** - Containerization platform
- **[Uvicorn](https://www.uvicorn.org/)** - Lightning-fast ASGI server
- **[Pydantic](https://pydantic-docs.helpmanual.io/)** - Data validation using Python type hints

## 🤝 Contributing

Contributions are welcome! Please feel free to submit a Pull Request.

1. Fork the repository
2. Create your feature branch (`git checkout -b feature/AmazingFeature`)
3. Commit your changes (`git commit -m 'Add some AmazingFeature'`)
4. Push to the branch (`git push origin feature/AmazingFeature`)
5. Open a Pull Request

## 📄 License

This project is licensed under the MIT License - see the [LICENSE](LICENSE) file for details.

## 👨‍💻 Author

**MAUREEN KARIMI**
- GitHub: [@Mkikii](https://github.com/Mkikii)
- Project Link: [https://github.com/Mkikii/genai-text-analyzer](https://github.com/Mkikii/genai-text-analyzer)

## 🙏 Acknowledgments

- [Moringa School](https://moringaschool.com/) for the AI Capstone Project framework
- [OpenAI](https://openai.com/) for providing the GPT API
- [FastAPI](https://fastapi.tiangolo.com/) community for excellent documentation

## 📞 Support

If you have any questions or run into issues, please open an issue on GitHub or contact the maintainer.

---
