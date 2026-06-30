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
    status: str
