from fastapi.testclient import TestClient
from app.main import app

client = TestClient(app)

def test_create_grade():
    response = client.post("/api/v1/grades/", json={
        "student_id": 1,
        "course_id": 1,
        "grade": 85.5,
        "semester": "2026-T1"
    })
    assert response.status_code == 200
    assert response.json()["grade"] == 85.5

def test_get_all_grades():
    response = client.get("/api/v1/grades/")
    assert response.status_code == 200
    assert isinstance(response.json(), list)

def test_get_grade():
    # First create
    create_response = client.post("/api/v1/grades/", json={
        "student_id": 2,
        "course_id": 1,
        "grade": 90.0,
        "semester": "2026-T1"
    })
    grade_id = create_response.json()["id"]

    # Then get
    response = client.get(f"/api/v1/grades/{grade_id}")
    assert response.status_code == 200
    assert response.json()["grade"] == 90.0

def test_update_grade():
    # First create
    create_response = client.post("/api/v1/grades/", json={
        "student_id": 3,
        "course_id": 2,
        "grade": 70.0,
        "semester": "2026-T1"
    })
    grade_id = create_response.json()["id"]

    # Then update
    response = client.put(f"/api/v1/grades/{grade_id}", json={
        "grade": 80.0
    })
    assert response.status_code == 200
    assert response.json()["grade"] == 80.0

def test_calculate_gpa():
    # Create student grades
    client.post("/api/v1/grades/", json={
        "student_id": 10,
        "course_id": 1,
        "grade": 80.0,
        "semester": "2026-T1"
    })
    client.post("/api/v1/grades/", json={
        "student_id": 10,
        "course_id": 2,
        "grade": 90.0,
        "semester": "2026-T1"
    })

    # Calculate GPA
    response = client.get("/api/v1/grades/student/10/gpa")
    assert response.status_code == 200
    assert response.json()["gpa"] == 85.0
    assert response.json()["total_courses"] == 2

def test_grade_not_found():
    response = client.get("/api/v1/grades/99999")
    assert response.status_code == 404

def test_delete_grade():
    # First create
    create_response = client.post("/api/v1/grades/", json={
        "student_id": 5,
        "course_id": 3,
        "grade": 75.0,
        "semester": "2026-T1"
    })
    grade_id = create_response.json()["id"]

    # Then delete
    response = client.delete(f"/api/v1/grades/{grade_id}")
    assert response.status_code == 200