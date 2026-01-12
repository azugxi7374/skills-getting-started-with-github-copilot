import pytest
from fastapi.testclient import TestClient
from src.app import app

client = TestClient(app)

def test_get_activities():
    response = client.get("/activities")
    assert response.status_code == 200
    data = response.json()
    assert isinstance(data, dict)
    assert "Soccer" in data

def test_signup_for_activity():
    response = client.post("/activities/Soccer/signup?email=test@example.com")
    assert response.status_code == 200
    assert "Signed up" in response.json()["message"]

def test_signup_duplicate():
    # First signup
    client.post("/activities/Basketball/signup?email=duplicate@example.com")
    # Second should fail
    response = client.post("/activities/Basketball/signup?email=duplicate@example.com")
    assert response.status_code == 400
    assert "already signed up" in response.json()["detail"]

def test_signup_nonexistent_activity():
    response = client.post("/activities/Nonexistent/signup?email=test@example.com")
    assert response.status_code == 404

def test_unregister_from_activity():
    # First signup
    client.post("/activities/Drama Club/signup?email=unregister@example.com")
    # Then unregister
    response = client.delete("/activities/Drama Club/signup?email=unregister@example.com")
    assert response.status_code == 200
    assert "Unregistered" in response.json()["message"]

def test_unregister_not_signed_up():
    response = client.delete("/activities/Art Studio/signup?email=notsigned@example.com")
    assert response.status_code == 400
    assert "not signed up" in response.json()["detail"]

def test_unregister_nonexistent_activity():
    response = client.delete("/activities/Nonexistent/signup?email=test@example.com")
    assert response.status_code == 404