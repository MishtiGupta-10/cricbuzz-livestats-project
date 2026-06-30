from fastapi import APIRouter, Depends, HTTPException, status
from typing import List

from backend.schemas.cricbuzz import LiveMatch, MatchInfo
from backend.services.match_service import MatchService
from backend.clients.cricbuzz import CricbuzzClient

router = APIRouter()

def get_match_service() -> MatchService:
    # In a real app with DB, we might inject a DB session here too.
    # For now, we inject the CricbuzzClient.
    client = CricbuzzClient()
    return MatchService(client)

@router.get(
    "/live",
    response_model=List[LiveMatch],
    summary="Get live matches",
    description="Fetches a list of currently live cricket matches.",
)
def get_live_matches(
    service: MatchService = Depends(get_match_service)
):
    """
    Returns live cricket matches.
    Exceptions are handled by global exception handlers in backend/core/errors.py.
    """
    return service.get_live_matches()


@router.get(
    "/recent",
    response_model=List[LiveMatch],
    summary="Get recent matches",
    description="Fetches a list of recently concluded cricket matches.",
)
def get_recent_matches(
    service: MatchService = Depends(get_match_service)
):
    """
    Returns recent cricket matches.
    """
    return service.get_recent_matches()


@router.get(
    "/{match_id}",
    response_model=MatchInfo,
    summary="Get match details",
    description="Fetches detailed information for a specific match ID.",
)
def get_match_details(
    match_id: int,
    service: MatchService = Depends(get_match_service)
):
    """
    Returns specific details for a match given its ID.
    """
    # Parameter validation is implicitly handled by FastAPI (match_id: int)
    return service.get_match_details(match_id)

@router.get(
    "/stored",
    summary="Get stored matches",
    description="Fetches all matches synchronized in the local database.",
)
def get_stored_matches():
    """
    Returns all matches stored locally, avoiding API calls.
    """
    from backend.database import repository
    return repository.get_all_matches()
