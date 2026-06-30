import pytest
import requests
from unittest.mock import patch, MagicMock
from backend.clients.cricbuzz import CricbuzzClient
from backend.core.exceptions import CricbuzzClientError, CricbuzzAPIError
from backend.schemas.cricbuzz import LiveMatch, MatchInfo

@patch("backend.clients.cricbuzz.requests.Session.request")
def test_get_live_matches_success(mock_request):
    mock_response = MagicMock()
    mock_response.json.return_value = {
        "typeMatches": [
            {
                "seriesMatches": [
                    {
                        "seriesAdWrapper": {
                            "seriesName": "Test Series",
                            "matches": [
                                {
                                    "matchInfo": {
                                        "matchId": 123,
                                        "team1": {"teamId": 1},
                                        "team2": {"teamId": 2}
                                    }
                                }
                            ]
                        }
                    }
                ]
            }
        ]
    }
    mock_response.raise_for_status.return_value = None
    mock_request.return_value = mock_response

    client = CricbuzzClient()
    matches = client.get_live_matches()
    
    assert len(matches) == 1
    assert isinstance(matches[0], LiveMatch)
    assert matches[0].match_id == 123

@patch("backend.clients.cricbuzz.requests.Session.request")
def test_get_match_info_success(mock_request):
    mock_response = MagicMock()
    mock_response.json.return_value = {
        "matchId": 456,
        "team1": {"teamId": 1},
        "team2": {"teamId": 2},
        "venueInfo": {"ground": "Test Ground"}
    }
    mock_response.raise_for_status.return_value = None
    mock_request.return_value = mock_response

    client = CricbuzzClient()
    match_info = client.get_match_info(456)
    
    assert isinstance(match_info, MatchInfo)
    assert match_info.match_id == 456
    assert match_info.venue.ground == "Test Ground"

@patch("backend.clients.cricbuzz.requests.Session.request")
def test_network_error(mock_request):
    mock_request.side_effect = requests.exceptions.ConnectionError("Connection Failed")
    client = CricbuzzClient()
    
    with pytest.raises(CricbuzzClientError):
        client.get_live_matches()

@patch("backend.clients.cricbuzz.requests.Session.request")
def test_http_error(mock_request):
    mock_response = MagicMock()
    
    http_error = requests.exceptions.HTTPError("404 Not Found")
    http_error.response = MagicMock()
    http_error.response.status_code = 404
    http_error.response.text = "Not Found"
    
    mock_response.raise_for_status.side_effect = http_error
    mock_request.return_value = mock_response
    
    client = CricbuzzClient()
    
    with pytest.raises(CricbuzzAPIError):
        client.get_live_matches()
