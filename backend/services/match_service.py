import logging
from typing import List

from backend.clients.cricbuzz import CricbuzzClient
from backend.schemas.cricbuzz import LiveMatch, MatchInfo
from backend.core.exceptions import CricInsightError

from backend.database.models import TeamModel, VenueModel, MatchModel, SyncLogModel
from backend.database import repository

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

    def sync_live_matches(self) -> List[MatchModel]:
        """Fetch live matches, enrich with MatchInfo, and sync to MySQL database."""
        logger.info("MatchService: Starting sync of live matches to database.")
        synced_matches = []
        try:
            live_matches = self.get_live_matches()
            
            for lm in live_matches:
                # We need full info for format and venue
                try:
                    match_info = self.get_match_details(lm.match_id)
                except Exception as e:
                    logger.warning(f"Failed to get match info for {lm.match_id}, skipping. Error: {e}")
                    continue
                
                # 1. Save Teams
                t1 = TeamModel(team_name=match_info.team1.team_name, short_name=match_info.team1.team_sname)
                t2 = TeamModel(team_name=match_info.team2.team_name, short_name=match_info.team2.team_sname)
                t1_saved = repository.save_team(t1)
                t2_saved = repository.save_team(t2)
                
                # 2. Save Venue
                v = VenueModel(venue_name=match_info.venue.ground, city=match_info.venue.city)
                v_saved = repository.save_venue(v)
                
                # 3. Save Match
                m = MatchModel(
                    match_id=match_info.match_id,
                    series_name=match_info.series_name,
                    match_description=match_info.match_desc,
                    format=match_info.match_format,
                    status=match_info.status,
                    state=match_info.state,
                    venue_id=v_saved.id,
                    team1_id=t1_saved.id,
                    team2_id=t2_saved.id
                )
                m_saved = repository.save_match(m)
                synced_matches.append(m_saved)
                
            # Log successful sync
            log = SyncLogModel(
                endpoint="/matches/v1/live",
                records_processed=len(synced_matches),
                status="Success"
            )
            repository.log_sync(log)
            
            return synced_matches
        
        except Exception as e:
            logger.error(f"MatchService sync failed: {e}")
            # Log failed sync
            log = SyncLogModel(
                endpoint="/matches/v1/live",
                records_processed=len(synced_matches),
                status=f"Failed: {str(e)}"
            )
            repository.log_sync(log)
            raise
