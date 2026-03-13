# Autonomous Car Mock Data – Pandas Practice Ideas

After running `python create_mock_data.py`, you get four CSV files in `data/`.

## Data Overview

| File | Rows | Description |
|------|------|-------------|
| `vehicles.csv` | 12 | Fleet: vehicle_id, model, manufacture_date, total_miles, last_maintenance_date |
| `trips.csv` | 500 | Trips: trip_id, vehicle_id, date, duration_min, distance_km, avg_speed_kmh, interventions, route_type, weather |
| `sensor_readings.csv` | ~10k | Per-trip samples: reading_id, trip_id, timestamp, speed_kmh, lat, lon, lidar_confidence, camera_status, objects_detected |
| `disengagements.csv` | 80 | Events: event_id, trip_id, timestamp, reason, location_type |

## Exercise Ideas

1. **Load & inspect**  
   `pd.read_csv()`, `.head()`, `.info()`, `.describe()`, `.dtypes`.

2. **Filtering**  
   Trips in rain/snow; trips with interventions > 0; sensor readings where `camera_status == 'degraded'` or `lidar_confidence < 0.8`.

3. **GroupBy & aggregation**  
   - Mean distance and intervention count by `route_type` or `weather`.  
   - Total miles per vehicle (from trips: sum of `distance_km` per `vehicle_id`).  
   - Disengagements per `reason` and per `location_type`.

4. **Merge**  
   Join trips with vehicles on `vehicle_id`; join disengagements with trips on `trip_id` to get vehicle and route_type for each event.

5. **Time series**  
   Set `date`/`timestamp` as index; resample trips by week or month (e.g. count trips, mean distance); plot trends.

6. **Pivot/crosstab**  
   Crosstab of disengagement `reason` vs `location_type`; pivot of avg interventions by `route_type` and `weather`.

7. **Cleanup**  
   Drop duplicates, handle missing values, convert date columns with `pd.to_datetime()`.

8. **Export**  
   Save filtered or aggregated results with `.to_csv()` or `.to_parquet()`.
