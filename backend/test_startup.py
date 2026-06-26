from fastapi.testclient import TestClient
from main import app

client = TestClient(app)

with client:
    response = client.get("/api/v1/health")
    print(f"Status Code: {response.status_code}")
    print(f"Response: {response.json()}")
