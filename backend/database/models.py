from pydantic import BaseModel
from typing import Optional
from datetime import datetime

class TeamModel(BaseModel):
    id: Optional[int] = None
    team_name: str
    short_name: str

class VenueModel(BaseModel):
    id: Optional[int] = None
    venue_name: str
    city: str

class MatchModel(BaseModel):
    match_id: int
    series_name: str
    match_description: Optional[str] = None
    format: str
    status: Optional[str] = None
    state: Optional[str] = None
    venue_id: int
    team1_id: int
    team2_id: int
    last_updated: Optional[datetime] = None

class SyncLogModel(BaseModel):
    id: Optional[int] = None
    sync_time: Optional[datetime] = None
    endpoint: str
    records_processed: int = 0
    inserted_count: int = 0
    updated_count: int = 0
    skipped_count: int = 0
    status: str
    error_message: Optional[str] = None
    duration_seconds: float = 0.0

class SyncSummary(BaseModel):
    total_processed: int = 0
    inserted: int = 0
    updated: int = 0
    skipped: int = 0
    duration: float = 0.0
    success: bool = True
    timestamp: datetime
    error_message: Optional[str] = None
