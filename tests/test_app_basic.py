from fastapi.testclient import TestClient
from src.app import app, activities

client = TestClient(app)


def test_get_activities_returns_200_and_payload():
    response = client.get("/activities")
    assert response.status_code == 200
    payload = response.json()
    # Should return a dict with activity names
    assert isinstance(payload, dict)
    assert "Chess Club" in payload


def test_signup_and_remove_participant_flow():
    activity = "Chess Club"
    test_email = "testuser@example.com"

    # Ensure not already signed up
    if test_email in activities[activity]["participants"]:
        activities[activity]["participants"].remove(test_email)

    # Signup
    response = client.post(f"/activities/{activity}/signup?email={test_email}")
    assert response.status_code == 200
    assert test_email in activities[activity]["participants"]

    # Duplicate signup should return 400
    response_dup = client.post(f"/activities/{activity}/signup?email={test_email}")
    assert response_dup.status_code == 400

    # Remove participant
    response_del = client.delete(f"/activities/{activity}/participant/{test_email}")
    assert response_del.status_code == 200
    assert test_email not in activities[activity]["participants"]


def test_remove_nonexistent_participant_returns_404():
    activity = "Chess Club"
    fake_email = "nope@example.com"
    # Ensure not present
    if fake_email in activities[activity]["participants"]:
        activities[activity]["participants"].remove(fake_email)

    response = client.delete(f"/activities/{activity}/participant/{fake_email}")
    assert response.status_code == 404
