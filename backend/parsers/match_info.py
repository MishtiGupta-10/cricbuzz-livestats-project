from typing import Dict, Any
from backend.schemas.cricbuzz import MatchInfo
from backend.parsers.common import parse_team, parse_venue
from backend.core.exceptions import CricbuzzParseError
import logging

logger = logging.getLogger(__name__)

def parse_match_info(data: Dict[str, Any]) -> MatchInfo:
    try:
        match_id = data.get("matchId", 0)
        team1_data = data.get("team1", {})
        team2_data = data.get("team2", {})
        venue_data = data.get("venueInfo", data.get("venueinfo", {}))
        
        return MatchInfo(
            match_id=match_id,
            series_name=data.get("seriesName", data.get("seriesname", "")),
            match_desc=data.get("matchDesc", data.get("matchdesc", "")),
            match_format=data.get("matchFormat", data.get("matchformat", "")),
            status=data.get("status", ""),
            state=data.get("state", ""),
            team1=parse_team(team1_data),
            team2=parse_team(team2_data),
            venue=parse_venue(venue_data)
        )
    except Exception as e:
        logger.error(f"Failed to parse match info: {e}")
        raise CricbuzzParseError(f"Failed to parse match info: {e}")
