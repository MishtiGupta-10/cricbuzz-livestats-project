-- Database schema for CricInsight.
-- Phase 3: Normalized MySQL tables for teams, players, venues, matches, scorecards, and sync logs.

CREATE TABLE IF NOT EXISTS venues (
    venue_id INT AUTO_INCREMENT PRIMARY KEY,
    name VARCHAR(150) NOT NULL,
    city VARCHAR(100) NOT NULL,
    country VARCHAR(100) NOT NULL,
    capacity INT
);

CREATE TABLE IF NOT EXISTS teams (
    team_id INT AUTO_INCREMENT PRIMARY KEY,
    name VARCHAR(100) NOT NULL UNIQUE,
    short_name VARCHAR(20) NOT NULL
);

CREATE TABLE IF NOT EXISTS players (
    player_id INT AUTO_INCREMENT PRIMARY KEY,
    team_id INT NOT NULL,
    name VARCHAR(150) NOT NULL,
    role VARCHAR(50),
    batting_style VARCHAR(50),
    bowling_style VARCHAR(50),
    FOREIGN KEY (team_id) REFERENCES teams(team_id)
);

CREATE TABLE IF NOT EXISTS matches (
    match_id INT AUTO_INCREMENT PRIMARY KEY,
    series_name VARCHAR(200) NOT NULL,
    match_format VARCHAR(20) NOT NULL,
    venue_id INT NOT NULL,
    team1_id INT NOT NULL,
    team2_id INT NOT NULL,
    match_date DATETIME NOT NULL,
    status VARCHAR(50) NOT NULL,
    winner_team_id INT,
    FOREIGN KEY (venue_id) REFERENCES venues(venue_id),
    FOREIGN KEY (team1_id) REFERENCES teams(team_id),
    FOREIGN KEY (team2_id) REFERENCES teams(team_id),
    FOREIGN KEY (winner_team_id) REFERENCES teams(team_id)
);

CREATE TABLE IF NOT EXISTS scorecards (
    scorecard_id INT AUTO_INCREMENT PRIMARY KEY,
    match_id INT NOT NULL,
    player_id INT NOT NULL,
    runs_scored INT DEFAULT 0,
    balls_faced INT DEFAULT 0,
    fours INT DEFAULT 0,
    sixes INT DEFAULT 0,
    overs_bowled FLOAT DEFAULT 0.0,
    runs_conceded INT DEFAULT 0,
    wickets_taken INT DEFAULT 0,
    maidens INT DEFAULT 0,
    FOREIGN KEY (match_id) REFERENCES matches(match_id),
    FOREIGN KEY (player_id) REFERENCES players(player_id)
);

CREATE TABLE IF NOT EXISTS sync_logs (
    log_id INT AUTO_INCREMENT PRIMARY KEY,
    sync_type VARCHAR(50) NOT NULL,
    sync_time DATETIME DEFAULT CURRENT_TIMESTAMP,
    status VARCHAR(20) NOT NULL,
    records_updated INT DEFAULT 0,
    error_message VARCHAR(500)
);

-- Indexes for fast analytics query execution
CREATE INDEX idx_player_team ON players(team_id);
CREATE INDEX idx_match_venue ON matches(venue_id);
CREATE INDEX idx_match_teams ON matches(team1_id, team2_id);
CREATE INDEX idx_scorecard_match ON scorecards(match_id);
CREATE INDEX idx_scorecard_player ON scorecards(player_id);
