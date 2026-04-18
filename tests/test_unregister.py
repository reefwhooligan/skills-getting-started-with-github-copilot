def test_unregister_success(client):
    """Test successful unregister from an activity"""
    # michael@mergington.edu is already in Chess Club
    email = "michael@mergington.edu"
    activity = "Chess Club"
    
    response = client.delete(f"/activities/{activity}/unregister?email={email}")
    assert response.status_code == 200
    data = response.json()
    assert "Unregistered" in data["message"]
    assert email in data["message"]
    
    # Verify participant was removed
    activities = client.get("/activities").json()
    assert email not in activities[activity]["participants"]


def test_unregister_activity_not_found(client):
    """Test unregister fails when activity doesn't exist"""
    response = client.delete("/activities/Fake Club/unregister?email=test@mergington.edu")
    assert response.status_code == 404
    data = response.json()
    assert "Activity not found" in data["detail"]


def test_unregister_participant_not_found(client):
    """Test unregister fails when participant is not in activity"""
    email = "notamember@mergington.edu"
    response = client.delete(f"/activities/Chess Club/unregister?email={email}")
    assert response.status_code == 404
    data = response.json()
    assert "Participant not found" in data["detail"]


def test_unregister_last_participant(client):
    """Test unregister works when removing the last participant"""
    # First signup a unique user to an activity
    email = "lastparticipant@mergington.edu"
    activity = "Basketball Team"
    
    # Sign up first
    signup_response = client.post(f"/activities/{activity}/signup?email={email}")
    assert signup_response.status_code == 200
    
    # Verify they're in the list
    activities = client.get("/activities").json()
    participants_before = len(activities[activity]["participants"])
    assert email in activities[activity]["participants"]
    
    # Unregister
    response = client.delete(f"/activities/{activity}/unregister?email={email}")
    assert response.status_code == 200
    
    # Verify removed
    activities = client.get("/activities").json()
    assert email not in activities[activity]["participants"]
    assert len(activities[activity]["participants"]) == participants_before - 1


def test_unregister_one_of_many_participants(client):
    """Test unregister when other participants remain"""
    # Chess Club has multiple participants
    email_to_remove = "daniel@mergington.edu"
    activity = "Chess Club"
    
    # Get participant list before
    activities = client.get("/activities").json()
    initial_count = len(activities[activity]["participants"])
    
    # Unregister one
    response = client.delete(f"/activities/{activity}/unregister?email={email_to_remove}")
    assert response.status_code == 200
    
    # Verify count decreased by 1
    activities = client.get("/activities").json()
    assert len(activities[activity]["participants"]) == initial_count - 1
    assert email_to_remove not in activities[activity]["participants"]
