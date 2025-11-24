import sys
import os
sys.path.append(os.path.join(os.path.dirname(__file__), '..'))

import uvicorn
from fastapi.testclient import TestClient

# Import the app module and get the app instance
from app import main
client = TestClient(main.app)

def test_health_check_simple():
    """Simple health check test"""
    response = client.get("/health")
    assert response.status_code == 200
    data = response.json()
    assert data["status"] == "healthy"
