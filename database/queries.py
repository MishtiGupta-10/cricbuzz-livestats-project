from sqlalchemy.orm import Session
from database.models import Venue, Team, Player, Match, Scorecard, SyncLog
from typing import List, Optional

def get_team_by_name(db: Session, name: str) -> Optional[Team]:
    return db.query(Team).filter(Team.name == name).first()

def get_all_teams(db: Session) -> List[Team]:
    return db.query(Team).all()

def create_team(db: Session, name: str, short_name: str) -> Team:
    team = Team(name=name, short_name=short_name)
    db.add(team)
    db.commit()
    db.refresh(team)
    return team

def get_player_by_name_and_team(db: Session, name: str, team_id: int) -> Optional[Player]:
    return db.query(Player).filter(Player.name == name, Player.team_id == team_id).first()

def create_player(db: Session, team_id: int, name: str, role: str = None, batting_style: str = None, bowling_style: str = None) -> Player:
    player = Player(team_id=team_id, name=name, role=role, batting_style=batting_style, bowling_style=bowling_style)
    db.add(player)
    db.commit()
    db.refresh(player)
    return player

def get_venue_by_name(db: Session, name: str) -> Optional[Venue]:
    return db.query(Venue).filter(Venue.name == name).first()

def create_venue(db: Session, name: str, city: str, country: str, capacity: int = None) -> Venue:
    venue = Venue(name=name, city=city, country=country, capacity=capacity)
    db.add(venue)
    db.commit()
    db.refresh(venue)
    return venue

def get_match_by_id(db: Session, match_id: int) -> Optional[Match]:
    return db.query(Match).filter(Match.match_id == match_id).first()

def log_sync(db: Session, sync_type: str, status: str, records_updated: int = 0, error_message: str = None) -> SyncLog:
    log = SyncLog(sync_type=sync_type, status=status, records_updated=records_updated, error_message=error_message)
    db.add(log)
    db.commit()
    db.refresh(log)
    return log
