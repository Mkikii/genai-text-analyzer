import requests
import json

BASE_URL = "http://localhost:8000"

def test_endpoint(endpoint, method="GET", data=None):
    url = f"{BASE_URL}{endpoint}"
    try:
        if method == "POST":
            response = requests.post(url, json=data)
        else:
            response = requests.get(url)
        
        print(f"{method} {endpoint}: Status {response.status_code}")
        if response.status_code == 200:
            print(f"Response: {json.dumps(response.json(), indent=2)}")
        else:
            print(f"Error: {response.text}")
        print("-" * 50)
    except Exception as e:
        print(f"Error calling {endpoint}: {e}")

# Test all endpoints
print("=== Testing GenAI Text Analyzer API ===\n")

test_endpoint("/health")
test_endpoint("/cache/stats")

# Test input validation
test_endpoint("/analyze", "POST", {"text": "This is perfect!"})
test_endpoint("/analyze", "POST", {"text": "hi"})  # Too short
test_endpoint("/analyze", "POST", {"text": "a" * 1001})  # Too long

test_endpoint("/cache/stats")  # Check stats again
