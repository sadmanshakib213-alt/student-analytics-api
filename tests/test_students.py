from fastapi.testclient import TestClient
from app.main import app

client = TestClient(app)

def test_root():
    response = client.get("/")
    assert response.status_code == 200
    assert response.json()["message"] == "Student Analytics API is running"

def test_health_check():
    response = client.get("/health")
    assert response.status_code == 200
    assert response.json()["status"] == "healthy"

def test_create_student():
    response = client.post("/api/v1/students/", json={
        "name": "John Doe",
        "email": "john@example.com",
        "age": 20,
        "role": "student"
    })
    assert response.status_code == 200
    assert response.json()["name"] == "John Doe"
    assert response.json()["email"] == "john@example.com"

def test_get_all_students():
    response = client.get("/api/v1/students/")
    assert response.status_code == 200
    assert isinstance(response.json(), list)

def test_get_student():
    # First create a student
    create_response = client.post("/api/v1/students/", json={
        "name": "Jane Doe",
        "email": "jane@example.com",
        "age": 22,
        "role": "student"
    })
    student_id = create_response.json()["id"]

    # Then get it
    response = client.get(f"/api/v1/students/{student_id}")
    assert response.status_code == 200
    assert response.json()["name"] == "Jane Doe"

def test_update_student():
    # First create
    create_response = client.post("/api/v1/students/", json={
        "name": "Update Me",
        "email": "update@example.com",
        "age": 25,
        "role": "student"
    })
    student_id = create_response.json()["id"]

    # Then update
    response = client.put(f"/api/v1/students/{student_id}", json={
        "name": "Updated Name"
    })
    assert response.status_code == 200
    assert response.json()["name"] == "Updated Name"

def test_delete_student():
    # First create
    create_response = client.post("/api/v1/students/", json={
        "name": "Delete Me",
        "email": "delete@example.com",
        "age": 23,
        "role": "student"
    })
    student_id = create_response.json()["id"]

    # Then delete
    response = client.delete(f"/api/v1/students/{student_id}")
    assert response.status_code == 200

def test_student_not_found():
    response = client.get("/api/v1/students/99999")
    assert response.status_code == 404