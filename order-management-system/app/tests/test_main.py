from fastapi.testclient import TestClient
from app.main import app

client = TestClient(app)

def test_root():
    response = client.get("/")
    assert response.status_code == 200
    assert response.json() == {"message": "Hello"}

def test_about():
    response = client.get("/about")
    assert response.status_code == 200
    assert response.json() == {"message": "This is the about page."}