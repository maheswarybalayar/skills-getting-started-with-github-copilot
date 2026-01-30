import pytest
from fastapi.testclient import TestClient
from src.app import app

client = TestClient(app)

def test_get_activities():
    response = client.get("/activities")
    assert response.status_code == 200
    data = response.json()
    assert isinstance(data, dict)
    assert "Basketball" in data

def test_signup_and_unregister():
    # Use a unique email to avoid conflicts
    test_email = "pytestuser@mergington.edu"
    activity = "Basketball"
    # Sign up
    response = client.post(f"/activities/{activity}/signup?email={test_email}")
    assert response.status_code == 200
    assert f"Signed up {test_email}" in response.json()["message"]
    # Unregister
    response = client.delete(f"/activities/{activity}/unregister?email={test_email}")
    assert response.status_code == 200
    assert f"Unregistered {test_email}" in response.json()["message"]

def test_signup_duplicate():
    activity = "Basketball"
    email = "alex@mergington.edu"  # already registered
    response = client.post(f"/activities/{activity}/signup?email={email}")
    assert response.status_code == 400
    assert "already signed up" in response.json()["detail"]

def test_signup_full():
    # Fill up an activity artificially
    activity = "Tennis"
    max_participants = 10
    # Add up to max
    for i in range(2, max_participants+1):
        email = f"test{i}@mergington.edu"
        client.post(f"/activities/{activity}/signup?email={email}")
    # Now try one more
    response = client.post(f"/activities/{activity}/signup?email=overflow@mergington.edu")
    assert response.status_code == 400
    assert "Activity is full" in response.json()["detail"]
