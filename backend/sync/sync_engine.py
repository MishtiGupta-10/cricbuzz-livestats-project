import logging
import time
from datetime import datetime

from backend.clients.cricbuzz import CricbuzzClient
from backend.database import repository
from backend.database.models import TeamModel, VenueModel, MatchModel, SyncLogModel, SyncSummary

logger = logging.getLogger(__name__)

class SyncEngine:
    def __init__(self, client: CricbuzzClient = None):
        self.client = client or CricbuzzClient()

    def sync_live_matches(self) -> SyncSummary:
        """Intelligently syncs live matches, tracking inserts, updates, and skips."""
        logger.info("SyncEngine: Starting intelligent sync of live matches.")
        
        start_time = time.time()
        summary = SyncSummary(timestamp=datetime.utcnow())
        
        try:
            live_matches = self.client.get_live_matches()
            summary.total_processed = len(live_matches)
            
            for lm in live_matches:
                # Fetch full MatchInfo
                try:
                    match_info = self.client.get_match_info(lm.match_id)
                except Exception as e:
                    logger.warning(f"Failed to get match info for {lm.match_id}, skipping. Error: {e}")
                    summary.skipped += 1
                    continue
                
                # 1. Upsert Teams
                t1 = TeamModel(team_name=match_info.team1.team_name, short_name=match_info.team1.team_sname)
                t2 = TeamModel(team_name=match_info.team2.team_name, short_name=match_info.team2.team_sname)
                t1_saved = repository.save_team(t1)
                t2_saved = repository.save_team(t2)
                
                # 2. Upsert Venue
                v = VenueModel(venue_name=match_info.venue.ground, city=match_info.venue.city)
                v_saved = repository.save_venue(v)
                
                # 3. Match Upsert Logic
                existing_match = repository.get_match(match_info.match_id)
                
                new_match_data = {
                    "series_name": match_info.series_name,
                    "match_description": match_info.match_desc,
                    "format": match_info.match_format,
                    "status": match_info.status,
                    "state": match_info.state,
                    "venue_id": v_saved.id,
                    "team1_id": t1_saved.id,
                    "team2_id": t2_saved.id
                }
                
                if existing_match:
                    # Detect changes
                    changed_fields = {}
                    for field, new_val in new_match_data.items():
                        old_val = getattr(existing_match, field)
                        if old_val != new_val:
                            changed_fields[field] = new_val
                            
                    if changed_fields:
                        repository.update_match_fields(match_info.match_id, changed_fields)
                        summary.updated += 1
                        logger.debug(f"Updated match {match_info.match_id} with fields: {list(changed_fields.keys())}")
                    else:
                        summary.skipped += 1
                else:
                    # Insert new match
                    m = MatchModel(match_id=match_info.match_id, **new_match_data)
                    repository.save_match(m)
                    summary.inserted += 1
            
            summary.duration = round(time.time() - start_time, 2)
            summary.success = True
            
            # Log to DB
            self._log_sync_to_db(summary, endpoint="/matches/v1/live")
            return summary
            
        except Exception as e:
            logger.error(f"SyncEngine failed: {e}")
            summary.duration = round(time.time() - start_time, 2)
            summary.success = False
            summary.error_message = str(e)
            
            # Log failure to DB
            self._log_sync_to_db(summary, endpoint="/matches/v1/live")
            return summary
            
    def _log_sync_to_db(self, summary: SyncSummary, endpoint: str):
        log = SyncLogModel(
            endpoint=endpoint,
            records_processed=summary.total_processed,
            inserted_count=summary.inserted,
            updated_count=summary.updated,
            skipped_count=summary.skipped,
            status="Success" if summary.success else "Failed",
            error_message=summary.error_message,
            duration_seconds=summary.duration
        )
        repository.log_sync(log)
