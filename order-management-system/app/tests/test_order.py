from fastapi.testclient import TestClient
from app.main import app
from app.schemas.order import OrderCreate, OrderUpdate

client = TestClient(app)

def test_create_order():
    order_data = {
        "customer_name": "John Doe",
        "items": ["Pizza", "Pasta"],
        "status": "pending"
    }
    response = client.post("/orders/", json=order_data)
    assert response.status_code == 201
    assert response.json()["customer_name"] == order_data["customer_name"]

def test_get_order():
    response = client.get("/orders/1")
    assert response.status_code == 200
    assert "customer_name" in response.json()

def test_update_order():
    update_data = {
        "status": "delivered"
    }
    response = client.put("/orders/1", json=update_data)
    assert response.status_code == 200
    assert response.json()["status"] == update_data["status"]

def test_get_nonexistent_order():
    response = client.get("/orders/999")
    assert response.status_code == 404

def test_create_order_invalid_data():
    order_data = {
        "customer_name": "",
        "items": [],
        "status": "pending"
    }
    response = client.post("/orders/", json=order_data)
    assert response.status_code == 422  # Unprocessable Entity for validation errors