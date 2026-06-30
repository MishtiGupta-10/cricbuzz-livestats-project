from fastapi import APIRouter, HTTPException, BackgroundTasks
from backend.sync.scheduler import scheduler
from backend.database.models import SyncSummary
from backend.database import repository

router = APIRouter()

@router.get("/status", summary="Get sync scheduler status")
async def get_sync_status():
    return {
        "scheduler_running": scheduler.is_running,
        "interval_minutes": scheduler.interval_seconds / 60,
        "job_running": scheduler._lock.locked()
    }

@router.post("/run", response_model=SyncSummary, summary="Run sync manually")
async def run_manual_sync():
    summary = await scheduler.run_sync()
    if not summary:
        raise HTTPException(status_code=409, detail="A sync job is already running.")
    return summary

@router.get("/history", summary="Get recent sync history")
async def get_sync_history(limit: int = 10):
    return repository.get_sync_history(limit)
