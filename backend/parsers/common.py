from typing import Dict, Any
from backend.schemas.cricbuzz import Team, Venue
from backend.core.exceptions import CricbuzzParseError
import logging

logger = logging.getLogger(__name__)

def parse_team(data: Dict[str, Any]) -> Team:
    try:
        return Team(
            teamId=data.get("teamId", data.get("teamId", 0)),
            teamName=data.get("teamName", data.get("teamname", "Unknown Team")),
            teamSName=data.get("teamSName", data.get("teamSName", "UNK")),
            imageId=data.get("imageId")
        )
    except Exception as e:
        logger.error(f"Failed to parse team: {e}")
        raise CricbuzzParseError(f"Failed to parse team: {e}")

def parse_venue(data: Dict[str, Any]) -> Venue:
    try:
        return Venue(
            ground=data.get("ground", "Unknown Ground"),
            city=data.get("city", "Unknown City"),
            timezone=data.get("timezone", ""),
            latitude=data.get("latitude", ""),
            longitude=data.get("longitude", "")
        )
    except Exception as e:
        logger.error(f"Failed to parse venue: {e}")
        raise CricbuzzParseError(f"Failed to parse venue: {e}")
