def test_get_activities(client):
    """Test GET /activities returns all activities"""
    response = client.get("/activities")
    assert response.status_code == 200
    activities = response.json()
    
    # Verify structure
    assert isinstance(activities, dict)
    assert len(activities) > 0


def test_get_activities_schema(client):
    """Test activity response has correct schema"""
    response = client.get("/activities")
    assert response.status_code == 200
    activities = response.json()
    
    # Check structure for all activities
    for activity_name, activity_data in activities.items():
        assert "description" in activity_data
        assert "schedule" in activity_data
        assert "max_participants" in activity_data
        assert "participants" in activity_data
        assert isinstance(activity_data["participants"], list)


def test_get_activities_known_activity(client):
    """Test a known activity exists with expected data"""
    response = client.get("/activities")
    activities = response.json()
    
    # Check Chess Club exists
    assert "Chess Club" in activities
    chess_club = activities["Chess Club"]
    assert chess_club["max_participants"] == 12
    assert isinstance(chess_club["participants"], list)
    assert len(chess_club["participants"]) > 0
