import logging
from typing import List, Optional

from backend.database.connection import get_db_connection
from backend.database.models import TeamModel, VenueModel, MatchModel, SyncLogModel

logger = logging.getLogger(__name__)

def save_team(team: TeamModel) -> TeamModel:
    query = """
        INSERT INTO team (team_name, short_name) 
        VALUES (%s, %s)
        ON DUPLICATE KEY UPDATE short_name = VALUES(short_name)
    """
    with get_db_connection() as conn:
        cursor = conn.cursor()
        cursor.execute(query, (team.team_name, team.short_name))
        conn.commit()
        
        # If it was a new insert, lastrowid will be set.
        # Otherwise we need to fetch it.
        if cursor.lastrowid:
            team.id = cursor.lastrowid
        else:
            cursor.execute("SELECT id FROM team WHERE team_name = %s", (team.team_name,))
            result = cursor.fetchone()
            if result:
                team.id = result[0]
                
    return team

def save_venue(venue: VenueModel) -> VenueModel:
    query = """
        INSERT INTO venue (venue_name, city) 
        VALUES (%s, %s)
        ON DUPLICATE KEY UPDATE venue_name = VALUES(venue_name)
    """
    with get_db_connection() as conn:
        cursor = conn.cursor()
        cursor.execute(query, (venue.venue_name, venue.city))
        conn.commit()
        
        if cursor.lastrowid:
            venue.id = cursor.lastrowid
        else:
            cursor.execute("SELECT id FROM venue WHERE venue_name = %s AND city = %s", (venue.venue_name, venue.city))
            result = cursor.fetchone()
            if result:
                venue.id = result[0]
                
    return venue

def save_match(match: MatchModel) -> MatchModel:
    query = """
        INSERT INTO `match` (match_id, series_name, match_description, format, status, state, venue_id, team1_id, team2_id)
        VALUES (%s, %s, %s, %s, %s, %s, %s, %s, %s)
        ON DUPLICATE KEY UPDATE
            series_name = VALUES(series_name),
            match_description = VALUES(match_description),
            format = VALUES(format),
            status = VALUES(status),
            state = VALUES(state),
            venue_id = VALUES(venue_id),
            team1_id = VALUES(team1_id),
            team2_id = VALUES(team2_id)
    """
    with get_db_connection() as conn:
        cursor = conn.cursor()
        cursor.execute(query, (
            match.match_id, match.series_name, match.match_description, 
            match.format, match.status, match.state, match.venue_id, 
            match.team1_id, match.team2_id
        ))
        conn.commit()
    return match

def update_match(match: MatchModel) -> MatchModel:
    # save_match acts as an upsert (insert on duplicate key update)
    # but providing an explicit update_match for repository completeness.
    query = """
        UPDATE `match`
        SET series_name = %s, match_description = %s, format = %s, 
            status = %s, state = %s, venue_id = %s, team1_id = %s, team2_id = %s
        WHERE match_id = %s
    """
    with get_db_connection() as conn:
        cursor = conn.cursor()
        cursor.execute(query, (
            match.series_name, match.match_description, match.format,
            match.status, match.state, match.venue_id, match.team1_id, match.team2_id,
            match.match_id
        ))
        conn.commit()
    return match

def match_exists(match_id: int) -> bool:
    query = "SELECT 1 FROM `match` WHERE match_id = %s"
    with get_db_connection() as conn:
        cursor = conn.cursor()
        cursor.execute(query, (match_id,))
        return cursor.fetchone() is not None

def get_match(match_id: int) -> Optional[MatchModel]:
    query = """
        SELECT match_id, series_name, match_description, format, status, state, 
               venue_id, team1_id, team2_id, last_updated 
        FROM `match` WHERE match_id = %s
    """
    with get_db_connection() as conn:
        cursor = conn.cursor(dictionary=True)
        cursor.execute(query, (match_id,))
        row = cursor.fetchone()
        if row:
            return MatchModel(**row)
    return None

def get_all_matches() -> List[MatchModel]:
    query = """
        SELECT match_id, series_name, match_description, format, status, state, 
               venue_id, team1_id, team2_id, last_updated 
        FROM `match`
    """
    matches = []
    with get_db_connection() as conn:
        cursor = conn.cursor(dictionary=True)
        cursor.execute(query)
        for row in cursor.fetchall():
            matches.append(MatchModel(**row))
    return matches

def update_match_fields(match_id: int, changed_fields: dict) -> None:
    if not changed_fields:
        return
    
    set_clause = ", ".join([f"{k} = %s" for k in changed_fields.keys()])
    values = list(changed_fields.values())
    values.append(match_id)
    
    query = f"UPDATE `match` SET {set_clause} WHERE match_id = %s"
    with get_db_connection() as conn:
        cursor = conn.cursor()
        cursor.execute(query, tuple(values))
        conn.commit()

def log_sync(log: SyncLogModel) -> SyncLogModel:
    query = """
        INSERT INTO synclog (endpoint, records_processed, inserted_count, updated_count, skipped_count, status, error_message, duration_seconds)
        VALUES (%s, %s, %s, %s, %s, %s, %s, %s)
    """
    with get_db_connection() as conn:
        cursor = conn.cursor()
        cursor.execute(query, (
            log.endpoint, log.records_processed, log.inserted_count, 
            log.updated_count, log.skipped_count, log.status, 
            log.error_message, log.duration_seconds
        ))
        conn.commit()
        if cursor.lastrowid:
            log.id = cursor.lastrowid
    return log

def get_sync_history(limit: int = 10) -> List[dict]:
    query = """
        SELECT id, sync_time, endpoint, records_processed, inserted_count, 
               updated_count, skipped_count, status, error_message, duration_seconds
        FROM synclog
        ORDER BY sync_time DESC
        LIMIT %s
    """
    history = []
    with get_db_connection() as conn:
        cursor = conn.cursor(dictionary=True)
        cursor.execute(query, (limit,))
        history = cursor.fetchall()
    return history
