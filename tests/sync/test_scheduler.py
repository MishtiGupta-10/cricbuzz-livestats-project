import unittest
import asyncio
from unittest.mock import patch, AsyncMock
from backend.sync.scheduler import SyncScheduler
from backend.database.models import SyncSummary
from datetime import datetime

class TestScheduler(unittest.IsolatedAsyncioTestCase):

    @patch('backend.sync.scheduler.SyncEngine')
    async def test_scheduler_starts_and_stops(self, mock_engine_class):
        scheduler = SyncScheduler()
        # Mock interval to be very small for test
        scheduler.interval_seconds = 0.1
        
        # Override the sync loop so it doesn't actually run forever in tests
        # We just want to test start/stop toggle logic
        
        await scheduler.start()
        self.assertTrue(scheduler.is_running)
        self.assertIsNotNone(scheduler._task)
        
        await scheduler.stop()
        self.assertFalse(scheduler.is_running)
        self.assertIsNone(scheduler._task)

    @patch('backend.sync.scheduler.SyncEngine')
    async def test_manual_sync_prevents_concurrency(self, mock_engine_class):
        mock_engine = mock_engine_class.return_value
        
        # We need sync_live_matches to be slow to test the lock
        def slow_sync():
            import time
            time.sleep(0.2)
            return SyncSummary(timestamp=datetime.utcnow(), total_processed=1)
            
        mock_engine.sync_live_matches = slow_sync
        
        scheduler = SyncScheduler()
        
        # Fire two concurrent manual syncs
        task1 = asyncio.create_task(scheduler.run_sync())
        task2 = asyncio.create_task(scheduler.run_sync())
        
        results = await asyncio.gather(task1, task2)
        
        # One should succeed and return a summary, the other should skip and return None
        success_count = sum(1 for r in results if r is not None)
        skip_count = sum(1 for r in results if r is None)
        
        self.assertEqual(success_count, 1)
        self.assertEqual(skip_count, 1)

if __name__ == '__main__':
    unittest.main()
