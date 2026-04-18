def test_signup_then_unregister(client):
    """Test signup followed by unregister in same session"""
    email = "integration@mergington.edu"
    activity = "Chess Club"
    
    # Sign up
    signup_response = client.post(f"/activities/{activity}/signup?email={email}")
    assert signup_response.status_code == 200
    
    # Verify added
    activities = client.get("/activities").json()
    assert email in activities[activity]["participants"]
    
    # Unregister
    unregister_response = client.delete(f"/activities/{activity}/unregister?email={email}")
    assert unregister_response.status_code == 200
    
    # Verify removed
    activities = client.get("/activities").json()
    assert email not in activities[activity]["participants"]


def test_signup_to_multiple_then_unregister_one(client):
    """Test signup to multiple activities then unregister from one"""
    email = "multitest@mergington.edu"
    activities_list = ["Chess Club", "Programming Class", "Gym Class"]
    
    # Sign up for all
    for activity in activities_list:
        response = client.post(f"/activities/{activity}/signup?email={email}")
        assert response.status_code == 200
    
    # Verify in all
    activities = client.get("/activities").json()
    for activity in activities_list:
        assert email in activities[activity]["participants"]
    
    # Unregister from one
    response = client.delete(f"/activities/{activities_list[0]}/unregister?email={email}")
    assert response.status_code == 200
    
    # Verify still in other two but not in first
    activities = client.get("/activities").json()
    assert email not in activities[activities_list[0]]["participants"]
    assert email in activities[activities_list[1]]["participants"]
    assert email in activities[activities_list[2]]["participants"]


def test_unregister_then_signup_same_activity(client):
    """Test unregister then re-signup to same activity"""
    email = "reregister@mergington.edu"
    activity = "Soccer Club"
    
    # Sign up
    response = client.post(f"/activities/{activity}/signup?email={email}")
    assert response.status_code == 200
    
    # Unregister
    response = client.delete(f"/activities/{activity}/unregister?email={email}")
    assert response.status_code == 200
    
    # Sign up again
    response = client.post(f"/activities/{activity}/signup?email={email}")
    assert response.status_code == 200
    
    # Verify back in activity
    activities = client.get("/activities").json()
    assert email in activities[activity]["participants"]


def test_activity_availability_updates_after_signup(client):
    """Test that availability count updates after signup"""
    email = "availability@mergington.edu"
    activity = "Art Studio"
    
    # Get initial availability
    activities_before = client.get("/activities").json()
    initial_count = len(activities_before[activity]["participants"])
    max_participants = activities_before[activity]["max_participants"]
    initial_available = max_participants - initial_count
    
    # Sign up
    response = client.post(f"/activities/{activity}/signup?email={email}")
    assert response.status_code == 200
    
    # Get updated availability
    activities_after = client.get("/activities").json()
    new_count = len(activities_after[activity]["participants"])
    new_available = max_participants - new_count
    
    # Verify availability decreased by 1
    assert new_available == initial_available - 1
    assert new_count == initial_count + 1
