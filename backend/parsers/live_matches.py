from typing import Dict, Any, List
from backend.schemas.cricbuzz import LiveMatch
from backend.parsers.common import parse_team
from backend.core.exceptions import CricbuzzParseError
import logging

logger = logging.getLogger(__name__)

def parse_live_matches(data: Dict[str, Any]) -> List[LiveMatch]:
    live_matches = []
    try:
        type_matches = data.get("typeMatches", [])
        for match_type in type_matches:
            series_matches = match_type.get("seriesMatches", [])
            for series in series_matches:
                series_wrapper = series.get("seriesAdWrapper")
                if not series_wrapper:
                    continue
                
                series_name = series_wrapper.get("seriesName", "Unknown Series")
                matches = series_wrapper.get("matches", [])
                
                for match in matches:
                    match_info = match.get("matchInfo", {})
                    
                    team1_data = match_info.get("team1", {})
                    team2_data = match_info.get("team2", {})
                    
                    live_match = LiveMatch(
                        match_id=match_info.get("matchId", 0),
                        match_desc=match_info.get("matchDesc", ""),
                        series_name=series_name,
                        team1=parse_team(team1_data),
                        team2=parse_team(team2_data),
                        status=match_info.get("status", ""),
                        state=match_info.get("state", "")
                    )
                    live_matches.append(live_match)
        return live_matches
    except Exception as e:
        logger.error(f"Failed to parse live matches: {e}")
        raise CricbuzzParseError(f"Failed to parse live matches: {e}")
