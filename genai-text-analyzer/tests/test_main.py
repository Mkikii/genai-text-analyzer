import pytest
import sys
import os

# Add the app directory to the Python path
sys.path.append(os.path.join(os.path.dirname(__file__), '..'))

from fastapi.testclient import TestClient
from app.main import app

client = TestClient(app)

def test_health_check():
    """Test health check endpoint"""
    response = client.get("/health")
    assert response.status_code == 200
    data = response.json()
    assert data["status"] == "healthy"
    assert "timestamp" in data
    assert data["version"] == "1.0.0"

def test_root_endpoint():
    """Test root endpoint"""
    response = client.get("/")
    assert response.status_code == 200
    data = response.json()
    assert data["message"] == "GenAI Text Analyzer API"

def test_analyze_text_too_short():
    """Test analysis with text that's too short"""
    response = client.post("/analyze", json={"text": "hi"})
    assert response.status_code == 400
    assert "at least 10 characters" in response.json()["detail"]

def test_analyze_text_too_long():
    """Test analysis with text that's too long"""
    long_text = "a" * 1001
    response = client.post("/analyze", json={"text": long_text})
    assert response.status_code == 400
    assert "less than 1000 characters" in response.json()["detail"]

def test_analyze_text_missing_api_key():
    """Test analysis when API key is missing"""
    # This test will work because we're not setting the API key
    response = client.post("/analyze", json={"text": "This is a test sentence for analysis."})
    # Should return 500 because API key is not configured
    assert response.status_code == 500

def test_docs_available():
    """Test that API documentation is available"""
    response = client.get("/docs")
    assert response.status_code == 200

def test_analyze_endpoint_exists():
    """Test that analyze endpoint exists in docs"""
    response = client.get("/openapi.json")
    assert response.status_code == 200
    openapi_spec = response.json()
    assert "/analyze" in openapi_spec["paths"]