import pytest
from fastapi.testclient import TestClient
from unittest.mock import MagicMock

from backend.main import app
from backend.api.routes.matches import get_match_service
from backend.services.match_service import MatchService
from backend.schemas.cricbuzz import LiveMatch, MatchInfo, Team, Venue

client = TestClient(app)

@pytest.fixture
def mock_match_service():
    service = MagicMock(spec=MatchService)
    
    mock_team1 = Team(teamId=1, teamName="India", teamSName="IND", imageId=1)
    mock_team2 = Team(teamId=2, teamName="Australia", teamSName="AUS", imageId=2)
    mock_venue = Venue(ground="MCG", city="Melbourne", timezone="AEST", latitude="1", longitude="1")
    
    mock_live = LiveMatch(
        match_id=1,
        match_desc="1st Test",
        series_name="Border Gavaskar Trophy",
        team1=mock_team1,
        team2=mock_team2,
        status="In Progress",
        state="Live"
    )
    mock_info = MatchInfo(
        match_id=1,
        series_name="Border Gavaskar Trophy",
        match_desc="1st Test",
        match_format="TEST",
        status="In Progress",
        state="Live",
        team1=mock_team1,
        team2=mock_team2,
        venue=mock_venue
    )
    
    service.get_live_matches.return_value = [mock_live]
    service.get_recent_matches.return_value = [mock_live]
    service.get_match_details.return_value = mock_info
    
    return service

def test_get_live_matches(mock_match_service):
    app.dependency_overrides[get_match_service] = lambda: mock_match_service
    response = client.get("/api/v1/matches/live")
    assert response.status_code == 200
    assert len(response.json()) == 1
    assert response.json()[0]["match_id"] == 1
    app.dependency_overrides.clear()

def test_get_recent_matches(mock_match_service):
    app.dependency_overrides[get_match_service] = lambda: mock_match_service
    response = client.get("/api/v1/matches/recent")
    assert response.status_code == 200
    assert len(response.json()) == 1
    app.dependency_overrides.clear()

def test_get_match_details(mock_match_service):
    app.dependency_overrides[get_match_service] = lambda: mock_match_service
    response = client.get("/api/v1/matches/1")
    assert response.status_code == 200
    assert response.json()["match_id"] == 1
    assert response.json()["series_name"] == "Border Gavaskar Trophy"
    app.dependency_overrides.clear()
