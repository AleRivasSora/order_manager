from fastapi.testclient import TestClient
from app.main import app

client = TestClient(app)

def test_create_order():
    
    order_data = {
        "customer_id": 1,
        "employee_id": 2,
        "status": "pending",
        "items": [
            {"item_id": 1, "quantity": 2},
            {"item_id": 2, "quantity": 1}
        ]
    }
    response = client.post("/orders/", json=order_data)
    assert response.status_code == 201
    assert response.json()["customer_id"] == order_data["customer_id"]
    assert len(response.json()["items"]) == len(order_data["items"])

def test_get_order():
    order_data = {
        "customer_id": 1,
        "employee_id": 2,
        "status": "pending",
        "items": [
            {"item_id": 1, "quantity": 2}
        ]
    }
    create_response = client.post("/orders/", json=order_data)
    assert create_response.status_code == 201
    order_id = create_response.json()["id"]

    response = client.get(f"/orders/{order_id}")
    assert response.status_code == 200
    assert response.json()["id"] == order_id

def test_update_order():
    order_data = {
        "customer_id": 1,
        "employee_id": 2,
        "status": "pending",
        "items": [
            {"item_id": 1, "quantity": 2}
        ]
    }
    create_response = client.post("/orders/", json=order_data)
    assert create_response.status_code == 201
    order_id = create_response.json()["id"]

    update_data = {
        "status": "completed",
        "employee_id": 3
    }
    response = client.put(f"/orders/{order_id}", json=update_data)
    assert response.status_code == 200
    assert response.json()["status"] == update_data["status"]
    assert response.json()["employee_id"] == update_data["employee_id"]

def test_get_nonexistent_order():
    response = client.get("/orders/999")
    assert response.status_code == 404

def test_create_order_invalid_data():
    order_data = {
        "customer_id": None,
        "items": [],
        "status": "invalid_status"
    }
    response = client.post("/orders/", json=order_data)
    assert response.status_code == 422

def test_delete_order():
    order_data = {
        "customer_id": 1,
        "employee_id": 2,
        "status": "pending",
        "items": [
            {"item_id": 1, "quantity": 2}
        ]
    }
    create_response = client.post("/orders/", json=order_data)
    assert create_response.status_code == 201
    order_id = create_response.json()["id"]

    delete_response = client.delete(f"/orders/{order_id}")
    assert delete_response.status_code == 200

    get_response = client.get(f"/orders/{order_id}")
    assert get_response.status_code == 404

def test_list_orders():
    order_data_1 = {
        "customer_id": 1,
        "employee_id": 2,
        "status": "pending",
        "items": [
            {"item_id": 1, "quantity": 2}
        ]
    }
    order_data_2 = {
        "customer_id": 2,
        "employee_id": 3,
        "status": "completed",
        "items": [
            {"item_id": 2, "quantity": 1}
        ]
    }
    client.post("/orders/", json=order_data_1)
    client.post("/orders/", json=order_data_2)

    response = client.get("/orders/")
    assert response.status_code == 200
    assert len(response.json()) >= 2