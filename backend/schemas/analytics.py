from pydantic import BaseModel
from typing import Optional, List
from datetime import datetime

class AnalyticsSummary(BaseModel):
    total_matches: int
    total_teams: int
    total_venues: int
    records_processed: int
    last_sync_time: Optional[datetime] = None
    average_sync_duration: Optional[float] = None

class TeamAnalytics(BaseModel):
    team_id: int
    team_name: str
    matches_played: int
    percentage_contribution: float

class AnalyticsFilter(BaseModel):
    format: Optional[str] = None
    venue_id: Optional[int] = None
