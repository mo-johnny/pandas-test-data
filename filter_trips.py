"""
Filter trips by route type and weather.
Edit the lists below to choose which route_type and weather to keep.
"""

import pandas as pd

trips = pd.read_csv("data/trips.csv")

# --- 1. Optional: only trips with interventions (like before)
# Uncomment to restrict to trips that had at least one intervention:
# trips = trips[trips["interventions"] > 0]

# --- 2. Choose which route types and weather to keep (empty = all)
ROUTE_TYPES = ["highway", "city", "mixed"]   # e.g. ["city", "highway"]
WEATHER = ["clear", "rain", "fog", "snow"]   # e.g. ["rain", "fog"]

# Filter by route type and weather
mask_route = trips["route_type"].isin(ROUTE_TYPES)
mask_weather = trips["weather"].isin(WEATHER)
filtered = trips[mask_route & mask_weather]

print(f"Trips matching route_type {ROUTE_TYPES} and weather {WEATHER}: {len(filtered)}\n")
print(filtered)

# --- 3. Breakdown: count by route_type and weather
print("\n--- Counts by route_type and weather ---")
counts = filtered.groupby(["route_type", "weather"]).size().unstack(fill_value=0)
print(counts)

# --- 4. % trips with 1+ interventions by each weather type (no graphs)
trips["has_intervention"] = trips["interventions"] >= 1
pct_by_weather = trips.groupby("weather")["has_intervention"].agg(["mean", "sum", "count"])
pct_by_weather["pct"] = (pct_by_weather["mean"] * 100).round(1)
pct_by_weather = pct_by_weather.reindex(["clear", "rain", "fog", "snow"]).dropna(how="all")

print("\n--- % of trips with 1+ interventions by weather type ---")
for w in pct_by_weather.index:
    row = pct_by_weather.loc[w]
    print(f"  {w:6}: {row['pct']:5.1f}%  (n = {int(row['count'])})")
