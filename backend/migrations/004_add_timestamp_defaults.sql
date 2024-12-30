-- Add default timestamps for created_at and updated_at
ALTER TABLE aois 
ALTER COLUMN created_at SET DEFAULT CURRENT_TIMESTAMP,
ALTER COLUMN updated_at SET DEFAULT CURRENT_TIMESTAMP;
