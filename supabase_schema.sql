-- 📦 Schéma SQL Simplifié (Single-User)

-- 1. Table Sleep Data
CREATE TABLE sleep_data (
    date DATE PRIMARY KEY,
    raw_data JSONB NOT NULL,
    created_at TIMESTAMP WITH TIME ZONE DEFAULT timezone('utc'::text, now())
);

-- 2. Table Daily Metrics
CREATE TABLE daily_metrics (
    date DATE PRIMARY KEY,
    steps INT,
    rhr INT,
    stress_avg INT,
    created_at TIMESTAMP WITH TIME ZONE DEFAULT timezone('utc'::text, now())
);

-- 3. Table Journal
CREATE TABLE journal_entries (
    date DATE PRIMARY KEY,
    tags TEXT[],
    note TEXT,
    created_at TIMESTAMP WITH TIME ZONE DEFAULT timezone('utc'::text, now())
);

-- Note: RLS est désactivé ou mis en "Public" pour un usage solo simplifié avec clé API masquée.
ALTER TABLE sleep_data DISABLE ROW LEVEL SECURITY;
ALTER TABLE daily_metrics DISABLE ROW LEVEL SECURITY;
ALTER TABLE journal_entries DISABLE ROW LEVEL SECURITY;
