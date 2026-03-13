"""
Generate mock dataset for an autonomous car company.
Run: python create_mock_data.py
Output: data/*.csv
"""

import pandas as pd
import numpy as np
from datetime import datetime, timedelta
import os

np.random.seed(42)

# --- Config ---
N_VEHICLES = 12
N_TRIPS = 500
N_SENSOR_READINGS_PER_TRIP = 20  # samples per trip
N_DISENGAGEMENTS = 80

MODELS = ["AV-200", "AV-300", "AV-400", "AV-500"]
ROUTE_TYPES = ["highway", "city", "mixed"]
WEATHER = ["clear", "rain", "fog", "snow"]
DISENGAGEMENT_REASONS = [
    "pedestrian_unexpected",
    "construction_zone",
    "sensor_occlusion",
    "software_limitation",
    "driver_override",
    "road_closure",
    "emergency_vehicle",
]

# --- 1. Vehicles ---
vehicle_ids = [f"V{i:03d}" for i in range(1, N_VEHICLES + 1)]
manufacture_dates = pd.date_range("2022-01-01", periods=N_VEHICLES, freq="ME")
vehicles = pd.DataFrame({
    "vehicle_id": vehicle_ids,
    "model": np.random.choice(MODELS, N_VEHICLES),
    "manufacture_date": manufacture_dates,
    "total_miles": np.random.randint(5_000, 95_000, N_VEHICLES),
    "last_maintenance_date": pd.to_datetime("2024-01-01") - pd.to_timedelta(np.random.randint(0, 90, N_VEHICLES), unit="D"),
})

# --- 2. Trips ---
trip_dates = pd.date_range("2024-06-01", "2024-12-01", periods=N_TRIPS)
trips = pd.DataFrame({
    "trip_id": [f"T{i:05d}" for i in range(1, N_TRIPS + 1)],
    "vehicle_id": np.random.choice(vehicle_ids, N_TRIPS),
    "date": trip_dates,
    "duration_min": np.random.lognormal(3, 1.2, N_TRIPS).clip(5, 180).astype(int),
    "distance_km": np.random.lognormal(2.5, 1, N_TRIPS).clip(2, 250).round(1),
    "avg_speed_kmh": np.random.normal(45, 15, N_TRIPS).clip(10, 120).round(1),
    "interventions": np.random.poisson(0.3, N_TRIPS),
    "route_type": np.random.choice(ROUTE_TYPES, N_TRIPS, p=[0.4, 0.35, 0.25]),
    "weather": np.random.choice(WEATHER, N_TRIPS, p=[0.6, 0.2, 0.15, 0.05]),
})
trips["date"] = pd.to_datetime(trips["date"])

# --- 3. Sensor readings (sample per trip) ---
rows = []
for _, t in trips.iterrows():
    tid = t["trip_id"]
    n = N_SENSOR_READINGS_PER_TRIP + np.random.randint(-5, 6)
    base_time = pd.to_datetime(t["date"]) + timedelta(hours=np.random.randint(6, 20))
    for i in range(n):
        ts = base_time + timedelta(seconds=i * (t["duration_min"] * 60 / max(n, 1)))
        rows.append({
            "reading_id": len(rows) + 1,
            "trip_id": tid,
            "timestamp": ts,
            "speed_kmh": np.clip(t["avg_speed_kmh"] + np.random.normal(0, 8), 0, 130),
            "lat": 37.7 + np.random.uniform(-0.1, 0.1),
            "lon": -122.4 + np.random.uniform(-0.1, 0.1),
            "lidar_confidence": np.clip(np.random.beta(8, 2), 0, 1).round(3),
            "camera_status": np.random.choice(["ok", "ok", "degraded", "ok"], p=[0.7, 0.2, 0.08, 0.02]),
            "objects_detected": np.random.poisson(12),
        })
sensor_readings = pd.DataFrame(rows)

# --- 4. Disengagements (subset of trips have events) ---
trip_ids_with_events = trips["trip_id"].sample(min(N_DISENGAGEMENTS, N_TRIPS), replace=True).values
disengagements = []
for i, tid in enumerate(trip_ids_with_events):
    t = trips[trips["trip_id"] == tid].iloc[0]
    base = pd.to_datetime(t["date"]) + timedelta(minutes=np.random.randint(0, max(1, t["duration_min"])))
    disengagements.append({
        "event_id": i + 1,
        "trip_id": tid,
        "timestamp": base + timedelta(seconds=np.random.randint(-30, 30)),
        "reason": np.random.choice(DISENGAGEMENT_REASONS),
        "location_type": np.random.choice(["intersection", "highway", "parking_lot", "residential"], p=[0.35, 0.3, 0.2, 0.15]),
    })
disengagements = pd.DataFrame(disengagements)

# --- Save ---
os.makedirs("data", exist_ok=True)
vehicles.to_csv("data/vehicles.csv", index=False)
trips.to_csv("data/trips.csv", index=False)
sensor_readings.to_csv("data/sensor_readings.csv", index=False)
disengagements.to_csv("data/disengagements.csv", index=False)

print("Created data/vehicles.csv")
print("Created data/trips.csv")
print("Created data/sensor_readings.csv")
print("Created data/disengagements.csv")
print("\nShapes:", vehicles.shape, trips.shape, sensor_readings.shape, disengagements.shape)
