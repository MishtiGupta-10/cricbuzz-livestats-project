import logging
from typing import List

from backend.clients.cricbuzz import CricbuzzClient
from backend.schemas.cricbuzz import LiveMatch, MatchInfo
from backend.core.exceptions import CricInsightError

logger = logging.getLogger(__name__)

class MatchService:
    def __init__(self, cricbuzz_client: CricbuzzClient):
        self.client = cricbuzz_client

    def get_live_matches(self) -> List[LiveMatch]:
        """Fetch all live matches from the client."""
        logger.info("MatchService: Fetching live matches.")
        try:
            return self.client.get_live_matches()
        except CricInsightError as e:
            logger.error(f"Failed to get live matches: {e}")
            raise

    def get_recent_matches(self) -> List[LiveMatch]:
        """Fetch all recent matches from the client."""
        logger.info("MatchService: Fetching recent matches.")
        try:
            return self.client.get_recent_matches()
        except CricInsightError as e:
            logger.error(f"Failed to get recent matches: {e}")
            raise

    def get_match_details(self, match_id: int) -> MatchInfo:
        """Fetch details for a specific match from the client."""
        logger.info(f"MatchService: Fetching match details for match_id={match_id}.")
        try:
            return self.client.get_match_info(match_id)
        except CricInsightError as e:
            logger.error(f"Failed to get match details for match_id={match_id}: {e}")
            raise
