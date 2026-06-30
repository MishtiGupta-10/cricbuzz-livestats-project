from sqlalchemy import Column, Integer, String, ForeignKey, DateTime, Float
from sqlalchemy.orm import relationship
from datetime import datetime
from database.database import Base

class Venue(Base):
    __tablename__ = "venues"

    venue_id = Column(Integer, primary_key=True, index=True)
    name = Column(String(150), nullable=False)
    city = Column(String(100), nullable=False)
    country = Column(String(100), nullable=False)
    capacity = Column(Integer, nullable=True)

    matches = relationship("Match", back_populates="venue")

class Team(Base):
    __tablename__ = "teams"

    team_id = Column(Integer, primary_key=True, index=True)
    name = Column(String(100), nullable=False, unique=True)
    short_name = Column(String(20), nullable=False)

    players = relationship("Player", back_populates="team")

class Player(Base):
    __tablename__ = "players"

    player_id = Column(Integer, primary_key=True, index=True)
    team_id = Column(Integer, ForeignKey("teams.team_id"), nullable=False, index=True)
    name = Column(String(150), nullable=False)
    role = Column(String(50), nullable=True)
    batting_style = Column(String(50), nullable=True)
    bowling_style = Column(String(50), nullable=True)

    team = relationship("Team", back_populates="players")
    scorecards = relationship("Scorecard", back_populates="player")

class Match(Base):
    __tablename__ = "matches"

    match_id = Column(Integer, primary_key=True, index=True)
    series_name = Column(String(200), nullable=False)
    match_format = Column(String(20), nullable=False)  # T20, ODI, Test
    venue_id = Column(Integer, ForeignKey("venues.venue_id"), nullable=False, index=True)
    team1_id = Column(Integer, ForeignKey("teams.team_id"), nullable=False, index=True)
    team2_id = Column(Integer, ForeignKey("teams.team_id"), nullable=False, index=True)
    match_date = Column(DateTime, nullable=False)
    status = Column(String(50), nullable=False)  # Live, Completed, Upcoming
    winner_team_id = Column(Integer, ForeignKey("teams.team_id"), nullable=True)

    venue = relationship("Venue", back_populates="matches")
    team1 = relationship("Team", foreign_keys=[team1_id])
    team2 = relationship("Team", foreign_keys=[team2_id])
    winner_team = relationship("Team", foreign_keys=[winner_team_id])
    scorecards = relationship("Scorecard", back_populates="match")

class Scorecard(Base):
    __tablename__ = "scorecards"

    scorecard_id = Column(Integer, primary_key=True, index=True)
    match_id = Column(Integer, ForeignKey("matches.match_id"), nullable=False, index=True)
    player_id = Column(Integer, ForeignKey("players.player_id"), nullable=False, index=True)
    
    # Batting Stats
    runs_scored = Column(Integer, default=0)
    balls_faced = Column(Integer, default=0)
    fours = Column(Integer, default=0)
    sixes = Column(Integer, default=0)
    
    # Bowling Stats
    overs_bowled = Column(Float, default=0.0)
    runs_conceded = Column(Integer, default=0)
    wickets_taken = Column(Integer, default=0)
    maidens = Column(Integer, default=0)

    match = relationship("Match", back_populates="scorecards")
    player = relationship("Player", back_populates="scorecards")

class SyncLog(Base):
    __tablename__ = "sync_logs"

    log_id = Column(Integer, primary_key=True, index=True)
    sync_type = Column(String(50), nullable=False)
    sync_time = Column(DateTime, default=datetime.utcnow)
    status = Column(String(20), nullable=False)  # Success, Failed
    records_updated = Column(Integer, default=0)
    error_message = Column(String(500), nullable=True)
