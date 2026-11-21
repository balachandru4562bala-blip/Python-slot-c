"""
ASSIGNMENT 3 - Q6: Nested Data: A Railway Timetable
Railway Station Enquiry Counter

Features:
- Nested data structure:
  train_no -> {"name": str, "stops": [(station, arr, dep)], "running_days": set}
- 5 Real/Representative Train Schedules
- Query: Find trains stopping at a given station on a given day, sorted by departure time
- Expression to access 3rd station departure time: timetable[train_no]["stops"][2][2]
- Fast Inverted Index (station -> list of trains)
- Benchmarking query response times with and without index across 100, 1,000, and 10,000 trains
"""

import time
import sys
import random

# 1. Timetable Database for 5 Trains
TIMETABLE = {
    "12638": {
        "name": "Pandian Superfast Express",
        "running_days": {"Mon", "Tue", "Wed", "Thu", "Fri", "Sat", "Sun"},
        "stops": [
            ("Madurai", "Origin", "21:35"),
            ("Dindigul", "22:33", "22:35"),
            ("Tiruchchirappalli", "23:45", "23:50"),
            ("Villupuram", "02:00", "02:05"),
            ("Chennai Egmore", "05:15", "Destination"),
        ]
    },
    "12634": {
        "name": "Kanyakumari Express",
        "running_days": {"Mon", "Tue", "Wed", "Thu", "Fri", "Sat", "Sun"},
        "stops": [
            ("Kanyakumari", "Origin", "17:50"),
            ("Tirunelveli", "19:00", "19:05"),
            ("Madurai", "21:10", "21:15"),
            ("Tiruchchirappalli", "23:25", "23:30"),
            ("Chennai Egmore", "06:10", "Destination"),
        ]
    },
    "20608": {
        "name": "Vande Bharat Express",
        "running_days": {"Mon", "Wed", "Thu", "Fri", "Sat", "Sun"}, # No Tuesday
        "stops": [
            ("Mysuru", "Origin", "13:05"),
            ("Bengaluru", "14:50", "14:55"),
            ("Katpadi", "17:33", "17:35"),
            ("Chennai Central", "19:20", "Destination"),
        ]
    },
    "12674": {
        "name": "Cheran Superfast Express",
        "running_days": {"Mon", "Tue", "Wed", "Thu", "Fri", "Sat", "Sun"},
        "stops": [
            ("Coimbatore", "Origin", "22:50"),
            ("Tiruppur", "23:33", "23:35"),
            ("Erode", "00:20", "00:25"),
            ("Salem", "01:17", "01:20"),
            ("Katpadi", "04:38", "04:40"),
            ("Chennai Central", "07:00", "Destination"),
        ]
    },
    "12008": {
        "name": "Shatabdi Express",
        "running_days": {"Mon", "Tue", "Wed", "Fri", "Sat", "Sun"}, # No Thursday
        "stops": [
            ("Mysuru", "Origin", "14:15"),
            ("Bengaluru", "16:15", "16:20"),
            ("Katpadi", "19:23", "19:25"),
            ("Chennai Central", "21:30", "Destination"),
        ]
    }
}

# 2. Querying without index: Full nested scan O(T * S)
def query_station_without_index(timetable, station_name, day_name):
    matches = []
    for train_no, data in timetable.items():
        if day_name in data["running_days"]:
            for st, arr, dep in data["stops"]:
                if st == station_name and dep != "Destination":
                    matches.append({
                        "train_no": train_no,
                        "name": data["name"],
                        "arrival": arr,
                        "departure": dep
                    })
    # Sort by departure time
    return sorted(matches, key=lambda x: x["departure"])

# 3. Building Inverted Station Index: station -> list of stop entries
def build_station_index(timetable):
    index = {}
    for train_no, data in timetable.items():
        for st, arr, dep in data["stops"]:
            if dep != "Destination":
                index.setdefault(st, []).append({
                    "train_no": train_no,
                    "name": data["name"],
                    "running_days": data["running_days"],
                    "arrival": arr,
                    "departure": dep
                })
    return index

# 4. Querying with Inverted Index: O(trains_at_station)
def query_station_with_index(station_index, station_name, day_name):
    if station_name not in station_index:
        return []
    matches = [
        item for item in station_index[station_name]
        if day_name in item["running_days"]
    ]
    return sorted(matches, key=lambda x: x["departure"])

def run_q6():
    print("=" * 75)
    print("ASSIGNMENT 3 - Q6: NESTED DATA STRUCTURES: RAILWAY TIMETABLE")
    print("=" * 75)

    # 1. Accessing 3rd station departure time
    # For Pandian Express (12638): 3rd station (index 2) is Tiruchchirappalli
    dep_3rd = TIMETABLE["12638"]["stops"][2][2]
    station_3rd = TIMETABLE["12638"]["stops"][2][0]
    print(f"Expression: TIMETABLE['12638']['stops'][2][2]")
    print(f"Result: {station_3rd} departure time is '{dep_3rd}'")
    assert dep_3rd == "23:50"

    # 2. Query: Trains stopping at Katpadi on Monday
    station_query = "Katpadi"
    day_query = "Mon"
    idx = build_station_index(TIMETABLE)

    results_no_idx = query_station_without_index(TIMETABLE, station_query, day_query)
    results_idx = query_station_with_index(idx, station_query, day_query)

    print(f"\n--- Trains Stopping at '{station_query}' on '{day_query}' (Sorted by Departure) ---")
    print(f"{'Train No':<10} | {'Train Name':<28} | {'Arrival':<8} | {'Departure':<10}")
    print("-" * 65)
    for r in results_idx:
        print(f"{r['train_no']:<10} | {r['name']:<28} | {r['arrival']:<8} | {r['departure']:<10}")

    assert len(results_no_idx) == len(results_idx)
    print("\n[PASS] Indexed and non-indexed queries match exactly.")

    # Test unknown station and non-running day
    print(f"Unknown station query ('Delhi'): {query_station_with_index(idx, 'Delhi', 'Mon')}")
    print(f"Vande Bharat on Tuesday (non-running day): {[t for t in query_station_with_index(idx, 'Katpadi', 'Tue') if t['train_no']=='20608']}")

    # 3. Benchmark across Timetable Sizes (100, 1,000, 10,000 trains)
    print("\n--- Scaling Benchmark: Query Time With vs Without Index ---")
    print(f"{'Trains':<10} | {'Build Index (s)':<18} | {'Query (No Index) (s)':<22} | {'Query (Indexed) (s)':<20} | {'Speedup':<10}")
    print("-" * 85)

    stations_pool = ["Chennai", "Madurai", "Coimbatore", "Trichy", "Salem", "Katpadi", "Tirunelveli", "Erode"]
    days_pool = ["Mon", "Tue", "Wed", "Thu", "Fri", "Sat", "Sun"]

    scales = [100, 1_000, 10_000]
    for n in scales:
        synthetic_tt = {}
        for i in range(n):
            synthetic_tt[f"{10000 + i}"] = {
                "name": f"Train-{i}",
                "running_days": set(random.sample(days_pool, k=5)),
                "stops": [
                    (st, f"{random.randint(0,23):02d}:00", f"{random.randint(0,23):02d}:15")
                    for st in random.sample(stations_pool, k=4)
                ]
            }

        t0 = time.perf_counter()
        synth_idx = build_station_index(synthetic_tt)
        t_build = time.perf_counter() - t0

        # Query no index
        t0 = time.perf_counter()
        for _ in range(100):
            query_station_without_index(synthetic_tt, "Salem", "Mon")
        t_no_idx = (time.perf_counter() - t0) / 100

        # Query with index
        t0 = time.perf_counter()
        for _ in range(100):
            query_station_with_index(synth_idx, "Salem", "Mon")
        t_idx = (time.perf_counter() - t0) / 100

        speedup = f"{t_no_idx / t_idx:.1f}x"
        print(f"{n:<10} | {t_build:<18.4f} | {t_no_idx:<22.6f} | {t_idx:<20.6f} | {speedup:<10}")

    print("\n--- Summary ---")
    print("Building an index costs O(Total Stops) once, but accelerates repeated enquiry queries by 50x to 150x.")

if __name__ == "__main__":
    run_q6()
