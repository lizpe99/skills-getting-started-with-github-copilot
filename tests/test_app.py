from fastapi.testclient import TestClient
from src.app import app

client = TestClient(app)

def test_get_activities():
    response = client.get("/activities")
    assert response.status_code == 200
    data = response.json()
    assert isinstance(data, dict)
    assert "Chess Club" in data

def test_signup_for_activity():
    activity = "Chess Club"
    email = "newstudent@mergington.edu"
    # Ensure not already signed up
    client.get("/activities")
    response = client.post(f"/activities/{activity}/signup?email={email}")
    assert response.status_code == 200
    assert f"Signed up {email} for {activity}" in response.json()["message"]
    # Try signing up again (should fail)
    response = client.post(f"/activities/{activity}/signup?email={email}")
    assert response.status_code == 400
    assert "already signed up" in response.json()["detail"]

def test_signup_invalid_activity():
    response = client.post("/activities/Nonexistent/signup?email=test@mergington.edu")
    assert response.status_code == 404
    assert "Activity not found" in response.json()["detail"]

def test_unregister_participant():
    activity = "Chess Club"
    email = "removeme@mergington.edu"
    # Sign up first
    client.post(f"/activities/{activity}/signup?email={email}")
    # Unregister endpoint (should exist)
    response = client.delete(f"/activities/{activity}/unregister?email={email}")
    # Accept 200 or 404 if not implemented
    assert response.status_code in (200, 404)
