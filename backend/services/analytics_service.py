import time
from typing import Optional, List, Dict, Any
from backend.database.connection import get_db_connection
from backend.schemas.analytics import AnalyticsSummary, TeamAnalytics, AnalyticsFilter

class AnalyticsService:
    _cache: Dict[str, Dict[str, Any]] = {}
    CACHE_TTL = 60

    @classmethod
    def _get_from_cache(cls, key: str) -> Optional[Any]:
        if key in cls._cache:
            entry = cls._cache[key]
            if time.time() - entry['timestamp'] < cls.CACHE_TTL:
                return entry['data']
        return None

    @classmethod
    def _set_in_cache(cls, key: str, data: Any):
        cls._cache[key] = {
            'timestamp': time.time(),
            'data': data
        }

    def get_summary(self, filters: Optional[AnalyticsFilter] = None) -> AnalyticsSummary:
        cache_key = f"summary_{filters.format if filters else ''}_{filters.venue_id if filters else ''}"
        cached = self._get_from_cache(cache_key)
        if cached:
            return cached

        where_clause = ""
        params = []
        if filters:
            conditions = []
            if filters.format:
                conditions.append("format = %s")
                params.append(filters.format)
            if filters.venue_id:
                conditions.append("venue_id = %s")
                params.append(filters.venue_id)
            if conditions:
                where_clause = "WHERE " + " AND ".join(conditions)
        
        query_matches = f"SELECT COUNT(*) FROM `match` {where_clause}"
        query_teams = "SELECT COUNT(*) FROM team"
        query_venues = "SELECT COUNT(*) FROM venue"
        query_sync = """
            SELECT SUM(records_processed), MAX(sync_time), AVG(duration_seconds)
            FROM synclog
        """

        with get_db_connection() as conn:
            cursor = conn.cursor()
            cursor.execute(query_matches, tuple(params))
            total_matches = cursor.fetchone()[0]

            cursor.execute(query_teams)
            total_teams = cursor.fetchone()[0]

            cursor.execute(query_venues)
            total_venues = cursor.fetchone()[0]

            cursor.execute(query_sync)
            sync_row = cursor.fetchone()
            records_processed = int(sync_row[0] or 0) if sync_row else 0
            last_sync_time = sync_row[1] if sync_row else None
            average_sync_duration = float(sync_row[2] or 0.0) if sync_row else 0.0

        summary = AnalyticsSummary(
            total_matches=total_matches,
            total_teams=total_teams,
            total_venues=total_venues,
            records_processed=records_processed,
            last_sync_time=last_sync_time,
            average_sync_duration=average_sync_duration
        )
        self._set_in_cache(cache_key, summary)
        return summary

    def get_team_analytics(self) -> List[TeamAnalytics]:
        cache_key = "team_analytics"
        cached = self._get_from_cache(cache_key)
        if cached:
            return cached
            
        query = """
            SELECT t.id, t.team_name, COUNT(m.match_id) as matches_played
            FROM team t
            LEFT JOIN `match` m ON t.id = m.team1_id OR t.id = m.team2_id
            GROUP BY t.id, t.team_name
            ORDER BY matches_played DESC
        """
        
        total_matches_query = "SELECT COUNT(*) FROM `match`"
        
        with get_db_connection() as conn:
            cursor = conn.cursor(dictionary=True)
            cursor.execute(total_matches_query)
            row = cursor.fetchone()
            total_matches = list(row.values())[0] if row else 0
            
            cursor.execute(query)
            teams_data = cursor.fetchall()
            
        result = []
        for row in teams_data:
            matches_played = row['matches_played']
            percentage = (matches_played / total_matches * 100) if total_matches > 0 else 0.0
            
            result.append(TeamAnalytics(
                team_id=row['id'],
                team_name=row['team_name'],
                matches_played=matches_played,
                percentage_contribution=round(percentage, 2)
            ))
            
        self._set_in_cache(cache_key, result)
        return result
