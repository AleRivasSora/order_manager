from unittest.mock import MagicMock
from fastapi.testclient import TestClient
from app.main import app
from app.controllers.user_controller import UserController

client = TestClient(app)

# Mock del controlador
mock_controller = MagicMock()

# Sobrescribir la dependencia para usar el mock
app.dependency_overrides[UserController] = lambda: mock_controller


def test_create_user():
    """
    Test creating a new user with mocked controller.
    """
    # Datos de entrada simulados
    user_data = {
        "username": "testuser",
        "email": "testuser@example.com",
        "password": "securepassword"
    }

    # Resultado esperado
    expected_response = {
        "id": 1,
        "username": "testuser",
        "email": "testuser@example.com"
    }

    # Configurar el mock para devolver el usuario esperado
    mock_controller.create_user.return_value = expected_response

    # Llamar a la ruta
    response = client.post("/users/", json=user_data)
    print(response.json())
    response_data = response.json()
    # Verificaciones
    assert response.status_code == 201
    assert "username" in response_data, "Response is missing 'username'"
    assert response_data["username"] == expected_response["username"], f"Expected username {expected_response['username']}, got {response_data['username']}"
    
    assert "email" in response_data, "Response is missing 'email'"
    assert response_data["email"] == expected_response["email"], f"Expected email {expected_response['email']}, got {response_data['email']}"
    mock_controller.create_user.assert_called_once_with(user_data)


def test_get_user():
    """
    Test retrieving a user by ID with mocked controller.
    """
    # ID del usuario a recuperar
    user_id = 1

    # Resultado esperado
    expected_response = {
        "id": user_id,
        "username": "testuser",
        "email": "testuser@example.com"
    }

    # Configurar el mock para devolver el usuario esperado
    mock_controller.get_user.return_value = expected_response

    # Llamar a la ruta
    response = client.get(f"/users/{user_id}")

    # Verificaciones
    assert response.status_code == 200
    assert response.json() == expected_response
    mock_controller.get_user.assert_called_once_with(user_id)


def test_update_user():
    """
    Test updating an existing user with mocked controller.
    """
    # ID del usuario a actualizar
    user_id = 1

    # Datos de entrada simulados
    update_data = {
        "username": "updateduser",
        "email": "updateduser@example.com"
    }

    # Resultado esperado
    expected_response = {
        "id": user_id,
        "username": "updateduser",
        "email": "updateduser@example.com"
    }

    # Configurar el mock para devolver el usuario actualizado
    mock_controller.update_user.return_value = expected_response

    # Llamar a la ruta
    response = client.put(f"/users/{user_id}", json=update_data)

    # Verificaciones
    assert response.status_code == 200
    assert response.json() == expected_response
    mock_controller.update_user.assert_called_once_with(user_id, update_data)


def test_list_users():
    """
    Test listing all users with mocked controller.
    """
    # Resultado esperado
    expected_response = [
        {"id": 1, "username": "testuser1", "email": "testuser1@example.com"},
        {"id": 2, "username": "testuser2", "email": "testuser2@example.com"}
    ]

    # Configurar el mock para devolver la lista de usuarios
    mock_controller.get_all_users.return_value = expected_response

    # Llamar a la ruta
    response = client.get("/users/")

    # Verificaciones
    assert response.status_code == 200
    assert response.json() == expected_response
    mock_controller.get_all_users.assert_called_once_with(skip=0, limit=10)


def test_create_user_with_existing_email():
    """
    Test creating a user with an email that already exists with mocked controller.
    """
    # Datos de entrada simulados
    user_data = {
        "username": "testuser",
        "email": "duplicate@example.com",
        "password": "securepassword"
    }

    # Configurar el mock para lanzar una excepción
    mock_controller.create_user.side_effect = Exception("Email already in use")

    # Llamar a la ruta
    response = client.post("/users/", json=user_data)

    # Verificaciones
    assert response.status_code == 500
    assert response.json()["detail"] == "Email already in use"
    mock_controller.create_user.assert_called_once_with(user_data)