import unittest
from unittest.mock import patch, MagicMock
from backend.database.models import TeamModel, VenueModel, MatchModel, SyncLogModel
from backend.database.repository import save_team, save_venue, save_match, update_match, log_sync

class TestDatabaseRepository(unittest.TestCase):

    @patch('backend.database.repository.get_db_connection')
    def test_save_team_inserts_correctly(self, mock_get_db):
        mock_conn = MagicMock()
        mock_cursor = MagicMock()
        mock_conn.cursor.return_value = mock_cursor
        mock_get_db.return_value.__enter__.return_value = mock_conn
        
        # Simulate insert returning an ID
        mock_cursor.lastrowid = 1
        
        team = TeamModel(team_name="India", short_name="IND")
        saved_team = save_team(team)
        
        self.assertEqual(saved_team.id, 1)
        mock_cursor.execute.assert_called_once()
        args, kwargs = mock_cursor.execute.call_args
        self.assertIn("INSERT INTO team", args[0])
        self.assertEqual(args[1], ("India", "IND"))
        mock_conn.commit.assert_called_once()

    @patch('backend.database.repository.get_db_connection')
    def test_save_team_duplicate_prevention(self, mock_get_db):
        mock_conn = MagicMock()
        mock_cursor = MagicMock()
        mock_conn.cursor.return_value = mock_cursor
        mock_get_db.return_value.__enter__.return_value = mock_conn
        
        # Simulate insert returning 0 (duplicate, updated)
        mock_cursor.lastrowid = 0
        mock_cursor.fetchone.return_value = (5,) # returns ID 5 from SELECT query
        
        team = TeamModel(team_name="Australia", short_name="AUS")
        saved_team = save_team(team)
        
        self.assertEqual(saved_team.id, 5)
        self.assertEqual(mock_cursor.execute.call_count, 2) # 1 for INSERT, 1 for SELECT

    @patch('backend.database.repository.get_db_connection')
    def test_save_match_insert_logic(self, mock_get_db):
        mock_conn = MagicMock()
        mock_cursor = MagicMock()
        mock_conn.cursor.return_value = mock_cursor
        mock_get_db.return_value.__enter__.return_value = mock_conn
        
        match = MatchModel(
            match_id=101,
            series_name="World Cup",
            format="ODI",
            venue_id=1,
            team1_id=1,
            team2_id=2
        )
        save_match(match)
        
        mock_cursor.execute.assert_called_once()
        args, kwargs = mock_cursor.execute.call_args
        self.assertIn("INSERT INTO `match`", args[0])
        self.assertIn("ON DUPLICATE KEY UPDATE", args[0])
        mock_conn.commit.assert_called_once()
        
    @patch('backend.database.repository.get_db_connection')
    def test_log_sync(self, mock_get_db):
        mock_conn = MagicMock()
        mock_cursor = MagicMock()
        mock_conn.cursor.return_value = mock_cursor
        mock_get_db.return_value.__enter__.return_value = mock_conn
        mock_cursor.lastrowid = 42
        
        log = SyncLogModel(endpoint="/api/test", records_processed=10, status="Success")
        saved_log = log_sync(log)
        
        self.assertEqual(saved_log.id, 42)
        mock_cursor.execute.assert_called_once()

if __name__ == '__main__':
    unittest.main()
