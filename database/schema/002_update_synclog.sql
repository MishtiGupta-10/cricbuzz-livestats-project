-- Phase 5: Update SyncLog schema for tracking sync statistics

ALTER TABLE synclog
ADD COLUMN inserted_count INT DEFAULT 0 AFTER records_processed,
ADD COLUMN updated_count INT DEFAULT 0 AFTER inserted_count,
ADD COLUMN skipped_count INT DEFAULT 0 AFTER updated_count,
ADD COLUMN error_message VARCHAR(500) AFTER status,
ADD COLUMN duration_seconds FLOAT DEFAULT 0.0 AFTER error_message;
