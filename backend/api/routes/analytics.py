from fastapi import APIRouter, Depends, Query
from typing import Optional, List
from backend.services.analytics_service import AnalyticsService
from backend.schemas.analytics import AnalyticsSummary, TeamAnalytics, AnalyticsFilter

router = APIRouter(prefix="/analytics", tags=["Analytics"])
analytics_service = AnalyticsService()

@router.get("/summary", response_model=AnalyticsSummary)
def get_analytics_summary(
    format: Optional[str] = Query(None, description="Filter by match format (e.g. T20)"),
    venue_id: Optional[int] = Query(None, description="Filter by venue ID")
):
    filters = AnalyticsFilter(format=format, venue_id=venue_id)
    return analytics_service.get_summary(filters=filters)

@router.get("/teams", response_model=List[TeamAnalytics])
def get_team_analytics():
    return analytics_service.get_team_analytics()
