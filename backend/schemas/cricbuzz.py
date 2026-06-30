from typing import Optional
from pydantic import BaseModel, Field


class Team(BaseModel):
    team_id: int = Field(alias="teamId")
    team_name: str = Field(alias="teamName")
    team_sname: str = Field(alias="teamSName")
    image_id: Optional[int] = Field(None, alias="imageId")


class Venue(BaseModel):
    ground: str
    city: str
    timezone: str
    latitude: str
    longitude: str


class Player(BaseModel):
    id: int
    name: str
    role: str
    batting_style: str = Field(alias="battingStyle")
    bowling_style: Optional[str] = Field(None, alias="bowlingStyle")


class LiveMatch(BaseModel):
    match_id: int
    match_desc: str
    series_name: str
    team1: Team
    team2: Team
    status: str
    state: str


class MatchInfo(BaseModel):
    match_id: int
    series_name: str
    match_desc: str
    match_format: str
    status: str
    state: str
    team1: Team
    team2: Team
    venue: Venue
