import pytest
from backend.parsers.live_matches import parse_live_matches
from backend.parsers.match_info import parse_match_info
from backend.core.exceptions import CricbuzzParseError

def test_parse_live_matches():
    sample_data = {
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
                                        "matchDesc": "1st Test",
                                        "team1": {"teamId": 1, "teamName": "India", "teamSName": "IND"},
                                        "team2": {"teamId": 2, "teamName": "Australia", "teamSName": "AUS"},
                                        "status": "In Progress",
                                        "state": "Live"
                                    }
                                }
                            ]
                        }
                    }
                ]
            }
        ]
    }
    
    matches = parse_live_matches(sample_data)
    assert len(matches) == 1
    match = matches[0]
    assert match.match_id == 123
    assert match.match_desc == "1st Test"
    assert match.series_name == "Test Series"
    assert match.team1.team_name == "India"
    assert match.team2.team_name == "Australia"
    assert match.status == "In Progress"

def test_parse_match_info():
    sample_data = {
        "matchId": 456,
        "seriesName": "T20 World Cup",
        "matchDesc": "Final",
        "matchFormat": "T20",
        "status": "Complete",
        "state": "Complete",
        "team1": {"teamId": 1, "teamname": "India", "teamSName": "IND"},
        "team2": {"teamId": 2, "teamname": "England", "teamSName": "ENG"},
        "venueInfo": {
            "ground": "MCG",
            "city": "Melbourne",
            "timezone": "+11:00",
            "latitude": "37.8",
            "longitude": "144.9"
        }
    }
    
    match_info = parse_match_info(sample_data)
    assert match_info.match_id == 456
    assert match_info.series_name == "T20 World Cup"
    assert match_info.match_format == "T20"
    assert match_info.team1.team_name == "India"
    assert match_info.venue.ground == "MCG"
    assert match_info.venue.city == "Melbourne"

def test_parse_live_matches_invalid_data():
    with pytest.raises(CricbuzzParseError):
        parse_live_matches({"typeMatches": [{"seriesMatches": "InvalidType"}]})
