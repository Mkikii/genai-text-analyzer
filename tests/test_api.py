import pytest
import sys
import os

# Add the app directory to the Python path
sys.path.append(os.path.join(os.path.dirname(__file__), '..'))

from fastapi.testclient import TestClient
from app.main import app

client = TestClient(app)

def test_health():
    """Test health endpoint returns 200 and correct structure"""
    response = client.get("/health")
    assert response.status_code == 200
    data = response.json()
    assert data["status"] == "healthy"
    assert "timestamp" in data
    assert data["version"] == "1.0.0"

def test_root_endpoint():
    """Test root endpoint returns Swagger UI"""
    response = client.get("/")
    assert response.status_code == 200
    assert "text/html" in response.headers["content-type"]

def test_analyze_text_validation():
    """Test text validation for analyze endpoint"""
    # Test too short text
    response = client.post("/analyze", json={"text": "hi"})
    assert response.status_code == 400
    
    # Test too long text
    long_text = "a" * 1001
    response = client.post("/analyze", json={"text": long_text})
    assert response.status_code == 400

def test_cache_endpoints():
    """Test cache management endpoints"""
    response = client.get("/cache/stats")
    assert response.status_code == 200
    data = response.json()
    assert "hit_rate" in data
    assert "total_requests" in data

def test_openapi_spec():
    """Test OpenAPI specification is available"""
    response = client.get("/openapi.json")
    assert response.status_code == 200
    spec = response.json()
    assert "paths" in spec
    assert "/analyze" in spec["paths"]
    assert "/health" in spec["paths"]
