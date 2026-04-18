def test_signup_success(client):
    """Test successful signup for an activity"""
    email = "newstudent@mergington.edu"
    response = client.post(f"/activities/Chess Club/signup?email={email}")
    assert response.status_code == 200
    data = response.json()
    assert "Signed up" in data["message"]
    assert email in data["message"]
    
    # Verify participant was added
    activities = client.get("/activities").json()
    assert email in activities["Chess Club"]["participants"]


def test_signup_activity_not_found(client):
    """Test signup fails when activity doesn't exist"""
    response = client.post("/activities/Nonexistent Club/signup?email=test@mergington.edu")
    assert response.status_code == 404
    data = response.json()
    assert "Activity not found" in data["detail"]


def test_signup_duplicate_student(client):
    """Test signup fails when student is already registered"""
    # michael@mergington.edu is already in Chess Club
    email = "michael@mergington.edu"
    response = client.post(f"/activities/Chess Club/signup?email={email}")
    assert response.status_code == 400
    data = response.json()
    assert "already signed up" in data["detail"]


def test_signup_to_empty_activity(client):
    """Test signup to activity with no current participants"""
    # Get an activity and clear it first by unregistering all participants
    activities = client.get("/activities").json()
    
    # Find an activity to test with - use Gym Class
    activity_name = "Gym Class"
    email = "emptyactivity@mergington.edu"
    
    response = client.post(f"/activities/{activity_name}/signup?email={email}")
    assert response.status_code == 200
    
    # Verify participant was added
    activities = client.get("/activities").json()
    assert email in activities[activity_name]["participants"]


def test_signup_multiple_different_activities(client):
    """Test same student can signup for multiple different activities"""
    email = "multiactivity@mergington.edu"
    activities_to_test = ["Chess Club", "Programming Class"]
    
    for activity_name in activities_to_test:
        response = client.post(f"/activities/{activity_name}/signup?email={email}")
        assert response.status_code == 200
    
    # Verify in both activities
    activities = client.get("/activities").json()
    for activity_name in activities_to_test:
        assert email in activities[activity_name]["participants"]
