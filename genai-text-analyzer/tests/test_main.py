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
    assert "redis_status" in data

def test_root_endpoint_returns_swagger_ui():
    """Test root endpoint returns Swagger UI HTML"""
    response = client.get("/")
    assert response.status_code == 200
    assert "text/html" in response.headers["content-type"]
    assert "Swagger UI" in response.text

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
    response = client.post("/analyze", json={"text": "This is a test sentence for analysis."})
    # Should return 502 (OpenAI error) or 500 (missing API key)
    assert response.status_code in [500, 502]

def test_openapi_spec_exists():
    """Test that OpenAPI spec is available"""
    response = client.get("/openapi.json")
    assert response.status_code == 200
    openapi_spec = response.json()
    assert "/analyze" in openapi_spec["paths"]
    assert "/health" in openapi_spec["paths"]
    assert "/cache/stats" in openapi_spec["paths"]

def test_cache_stats_endpoint():
    """Test cache stats endpoint"""
    response = client.get("/cache/stats")
    assert response.status_code == 200
    data = response.json()
    assert "total_requests" in data
    assert "cache_hits" in data
    assert "cache_misses" in data
    assert "hit_rate" in data
