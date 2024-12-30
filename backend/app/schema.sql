CREATE EXTENSION IF NOT EXISTS postgis;

CREATE TABLE aois (
    id SERIAL PRIMARY KEY,
    name TEXT NOT NULL,
    description TEXT,
    geometry GEOGRAPHY(POLYGON, 4326) NOT NULL,
    created_at TIMESTAMPTZ DEFAULT CURRENT_TIMESTAMP,
    updated_at TIMESTAMPTZ DEFAULT CURRENT_TIMESTAMP
);

CREATE TABLE export_tasks (
    id SERIAL PRIMARY KEY,
    aoi_id INTEGER REFERENCES aois(id),
    status TEXT NOT NULL,
    start_date DATE NOT NULL,
    end_date DATE NOT NULL,
    created_at TIMESTAMPTZ DEFAULT CURRENT_TIMESTAMP,
    updated_at TIMESTAMPTZ DEFAULT CURRENT_TIMESTAMP,
    task_id TEXT UNIQUE,
    error_message TEXT
);

-- Function to update updated_at timestamp
CREATE OR REPLACE FUNCTION update_updated_at_column()
RETURNS TRIGGER AS $$
BEGIN
    NEW.updated_at = CURRENT_TIMESTAMP;
    RETURN NEW;
END;
$$ language 'plpgsql';

-- Trigger for aois table
CREATE TRIGGER update_aois_updated_at
    BEFORE UPDATE ON aois
    FOR EACH ROW
    EXECUTE FUNCTION update_updated_at_column();

-- Trigger for export_tasks table
CREATE TRIGGER update_export_tasks_updated_at
    BEFORE UPDATE ON export_tasks
    FOR EACH ROW
    EXECUTE FUNCTION update_updated_at_column();