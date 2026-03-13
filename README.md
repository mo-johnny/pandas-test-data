# Autonomous Car Mock Dataset

Mock data for practicing **pandas** analysis in the context of an autonomous vehicle fleet.

## Setup

If `pip` isn’t found, use Python’s module form:

```bash
python3 -m pip install -r requirements.txt
python3 create_mock_data.py
```

**Optional – virtual environment** (avoids permission issues):

```bash
python3 -m venv .venv
source .venv/bin/activate   # on Windows: .venv\Scripts\activate
pip install -r requirements.txt
python create_mock_data.py
```

This creates a `data/` folder with four CSV files.

## Data Files

- **vehicles.csv** – Fleet (12 vehicles): id, model, manufacture date, total miles, last maintenance
- **trips.csv** – 500 trips: vehicle, date, duration, distance, speed, interventions, route_type, weather
- **sensor_readings.csv** – ~10k rows: per-trip samples with speed, GPS, lidar confidence, camera status, object counts
- **disengagements.csv** – 80 events: trip, timestamp, reason (e.g. pedestrian_unexpected, construction_zone), location_type

See **analysis_exercises.md** for concrete pandas exercise ideas (filtering, groupby, merge, time series, pivot).
