# Weather ETL

This repository contains a small ETL that pulls hourly weather data for a list of cities from the Open-Meteo API and writes it into a Postgres table `weather_raw`. A PySpark notebook demonstrates reading the raw table, aggregating daily statistics, and writing a cleaned `weather_clean` table.

Contents

- `etl.py` - Python ETL script that fetches hourly weather and inserts into Postgres.
- `de.ipynb` - Notebook which contains the ETL and PySpark transformations (already included).
- `requirements.txt` - Python dependencies for running the ETL and notebook.

Quick start

1. Create the database and table (example):

```sql
CREATE DATABASE weather;
\c weather

CREATE TABLE weather_raw (
  id SERIAL PRIMARY KEY,
  city TEXT NOT NULL,
  latitude DOUBLE PRECISION,
  longitude DOUBLE PRECISION,
  timestamp TIMESTAMP,
  temperature DOUBLE PRECISION,
  humidity DOUBLE PRECISION
);

CREATE TABLE weather_clean (
    city VARCHAR(50),
    date DATE,
    avg_temperature FLOAT,
    avg_humidity FLOAT
);
```

2. (Optional but recommended) Add a unique constraint to prevent duplicate city+timestamp rows:

```sql
ALTER TABLE weather_raw ADD CONSTRAINT weather_raw_city_timestamp_key UNIQUE (city, timestamp);
```

3. Install dependencies:

```bash
python -m venv .venv
source .venv/bin/activate
pip install -r requirements.txt
```
