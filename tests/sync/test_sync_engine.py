import unittest
from unittest.mock import patch, MagicMock
from backend.sync.sync_engine import SyncEngine
from backend.database.models import MatchModel
from backend.schemas.cricbuzz import LiveMatch, MatchInfo, Team, Venue

class TestSyncEngine(unittest.TestCase):

    @patch('backend.sync.sync_engine.repository')
    @patch('backend.sync.sync_engine.CricbuzzClient')
    def test_sync_engine_inserts_and_updates(self, MockClient, mock_repo):
        # Setup mock client data
        mock_client = MockClient.return_value
        
        # Two live matches
        lm1 = MagicMock(spec=LiveMatch)
        lm1.match_id = 101
        lm2 = MagicMock(spec=LiveMatch)
        lm2.match_id = 102
        
        mock_client.get_live_matches.return_value = [lm1, lm2]
        
        # Match Info for both
        mi1 = MagicMock(spec=MatchInfo)
        mi1.match_id = 101
        mi1.series_name = "Test Series"
        mi1.match_desc = "Match 1"
        mi1.match_format = "T20"
        mi1.status = "Live"
        mi1.state = "In Progress"
        mi1.team1 = MagicMock(spec=Team, team_name="Team A", team_sname="TA")
        mi1.team2 = MagicMock(spec=Team, team_name="Team B", team_sname="TB")
        mi1.venue = MagicMock(spec=Venue, ground="Stadium 1", city="City 1")
        
        mi2 = MagicMock(spec=MatchInfo)
        mi2.match_id = 102
        mi2.series_name = "Test Series"
        mi2.match_desc = "Match 2"
        mi2.match_format = "ODI"
        mi2.status = "Completed"
        mi2.state = "Complete"
        mi2.team1 = MagicMock(spec=Team, team_name="Team C", team_sname="TC")
        mi2.team2 = MagicMock(spec=Team, team_name="Team D", team_sname="TD")
        mi2.venue = MagicMock(spec=Venue, ground="Stadium 2", city="City 2")
        
        mock_client.get_match_info.side_effect = [mi1, mi2]
        
        # Setup mock repository behavior
        # Match 1 doesn't exist -> Insert
        # Match 2 exists and is different -> Update
        
        existing_m2 = MatchModel(
            match_id=102, series_name="Test Series", match_description="Match 2",
            format="ODI", status="Live", state="In Progress", venue_id=1, team1_id=1, team2_id=2
        )
        
        # get_match returns None for 101, existing_m2 for 102
        def mock_get_match(mid):
            if mid == 101:
                return None
            return existing_m2
            
        mock_repo.get_match.side_effect = mock_get_match
        
        # Dummy save returns for team and venue
        mock_repo.save_team.return_value = MagicMock(id=1)
        mock_repo.save_venue.return_value = MagicMock(id=1)
        
        # Run Sync
        engine = SyncEngine(client=mock_client)
        summary = engine.sync_live_matches()
        
        self.assertTrue(summary.success)
        self.assertEqual(summary.total_processed, 2)
        self.assertEqual(summary.inserted, 1) # Match 101
        self.assertEqual(summary.updated, 1) # Match 102 changed status
        self.assertEqual(summary.skipped, 0)
        
        mock_repo.save_match.assert_called_once()
        mock_repo.update_match_fields.assert_called_once()
        mock_repo.log_sync.assert_called_once()

if __name__ == '__main__':
    unittest.main()
