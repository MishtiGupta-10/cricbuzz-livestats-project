import asyncio
import logging
from typing import Optional

from backend.core.config import settings
from backend.sync.sync_engine import SyncEngine

logger = logging.getLogger(__name__)

class SyncScheduler:
    def __init__(self):
        self.engine = SyncEngine()
        self.interval_seconds = settings.sync_interval_minutes * 60
        self.is_running = False
        self._task: Optional[asyncio.Task] = None
        self._lock = asyncio.Lock()

    async def _sync_loop(self):
        """Background loop to periodically trigger synchronization."""
        logger.info(f"SyncScheduler: Started background loop (Interval: {settings.sync_interval_minutes}m)")
        while self.is_running:
            await self.run_sync()
            await asyncio.sleep(self.interval_seconds)

    async def start(self):
        """Start the background scheduler."""
        if self.is_running:
            logger.warning("SyncScheduler is already running.")
            return
        
        self.is_running = True
        self._task = asyncio.create_task(self._sync_loop())

    async def stop(self):
        """Stop the background scheduler."""
        if not self.is_running:
            return
        
        logger.info("SyncScheduler: Stopping background loop.")
        self.is_running = False
        if self._task:
            self._task.cancel()
            try:
                await self._task
            except asyncio.CancelledError:
                pass
            self._task = None

    async def run_sync(self):
        """Trigger a manual or scheduled synchronization, preventing concurrency."""
        if self._lock.locked():
            logger.warning("SyncScheduler: Sync job is already running. Skipping concurrent execution.")
            return None
        
        async with self._lock:
            # We run the synchronous sync_live_matches in a thread pool to avoid blocking the asyncio event loop
            try:
                logger.info("SyncScheduler: Executing sync engine...")
                summary = await asyncio.to_thread(self.engine.sync_live_matches)
                logger.info(f"SyncScheduler: Sync finished. {summary.inserted} inserted, {summary.updated} updated, {summary.skipped} skipped.")
                return summary
            except Exception as e:
                logger.error(f"SyncScheduler: Sync job failed gracefully: {e}")
                return None

# Global instance
scheduler = SyncScheduler()
