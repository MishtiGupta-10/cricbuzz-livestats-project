-- Phase 4: Database Schema for CricInsight
-- Normalized tables for Team, Venue, Match, and SyncLog

CREATE TABLE IF NOT EXISTS team (
    id INT AUTO_INCREMENT PRIMARY KEY,
    team_name VARCHAR(100) NOT NULL UNIQUE,
    short_name VARCHAR(20) NOT NULL
);

CREATE TABLE IF NOT EXISTS venue (
    id INT AUTO_INCREMENT PRIMARY KEY,
    venue_name VARCHAR(150) NOT NULL,
    city VARCHAR(100) NOT NULL,
    UNIQUE(venue_name, city)
);

CREATE TABLE IF NOT EXISTS `match` (
    match_id INT PRIMARY KEY, -- Using Cricbuzz match ID
    series_name VARCHAR(200) NOT NULL,
    match_description VARCHAR(200),
    format VARCHAR(20) NOT NULL,
    status VARCHAR(100),
    state VARCHAR(50),
    venue_id INT NOT NULL,
    team1_id INT NOT NULL,
    team2_id INT NOT NULL,
    last_updated DATETIME DEFAULT CURRENT_TIMESTAMP ON UPDATE CURRENT_TIMESTAMP,
    FOREIGN KEY (venue_id) REFERENCES venue(id),
    FOREIGN KEY (team1_id) REFERENCES team(id),
    FOREIGN KEY (team2_id) REFERENCES team(id)
);

CREATE TABLE IF NOT EXISTS synclog (
    id INT AUTO_INCREMENT PRIMARY KEY,
    sync_time DATETIME DEFAULT CURRENT_TIMESTAMP,
    endpoint VARCHAR(100) NOT NULL,
    records_processed INT DEFAULT 0,
    status VARCHAR(50) NOT NULL
);

-- Indexes
CREATE INDEX idx_match_venue ON `match`(venue_id);
CREATE INDEX idx_match_teams ON `match`(team1_id, team2_id);
CREATE INDEX idx_synclog_time ON synclog(sync_time);
