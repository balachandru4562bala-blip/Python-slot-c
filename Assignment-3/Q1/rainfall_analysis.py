"""
ASSIGNMENT 3 - Q1: Lists and Slicing: Daily Rainfall Records
Village Rain-Gauge Station

Features:
- Daily rainfall records for a year (365 days)
- Weekly totals using slicing readings[i:i+7]
- Wettest and driest weeks with start day and index
- 7-day moving average: Naive slicing vs Running-sum algorithm
- Derivation and empirical timing for 365, 36,500, and 365,000 readings
- Handling late arrivals (list.insert cost analysis)
- Edge cases: empty list, < 7 readings
- Alternative concepts: collections.deque(maxlen=7) vs dict keyed by date
"""

import random
import time
import collections
import sys

def compute_weekly_totals(readings):
    """Computes total rainfall for each of the 52 full weeks using slicing."""
    weekly_totals = []
    for week_idx in range(52):
        start = week_idx * 7
        end = start + 7
        week_slice = readings[start:end]
        weekly_totals.append((week_idx + 1, sum(week_slice)))
    return weekly_totals

def find_extreme_weeks(weekly_totals):
    """Finds wettest and driest weeks with their positions."""
    if not weekly_totals:
        return None, None
    wettest = max(weekly_totals, key=lambda x: x[1])
    driest = min(weekly_totals, key=lambda x: x[1])
    return wettest, driest

def moving_average_naive(readings, window=7):
    """Naive moving average: Slices window and re-sums for every day."""
    n = len(readings)
    if n < window:
        return []
    ma = []
    for i in range(n - window + 1):
        ma.append(sum(readings[i:i + window]) / window)
    return ma

def moving_average_running_sum(readings, window=7):
    """Running-sum moving average: Slide window by subtracting left and adding right."""
    n = len(readings)
    if n < window:
        return []
    curr_sum = sum(readings[:window])
    ma = [curr_sum / window]
    for i in range(window, n):
        curr_sum += readings[i] - readings[i - window]
        ma.append(curr_sum / window)
    return ma

def moving_average_deque(readings, window=7):
    """Alternative concept: Using collections.deque(maxlen=7)."""
    n = len(readings)
    if n < window:
        return []
    d = collections.deque(readings[:window], maxlen=window)
    curr_sum = sum(d)
    ma = [curr_sum / window]
    for val in readings[window:]:
        leaving = d[0]
        d.append(val)
        curr_sum += val - leaving
        ma.append(curr_sum / window)
    return ma

def get_dry_days(readings):
    """Returns indices of days with 0.0 mm rainfall."""
    return [day_idx + 1 for day_idx, rain in enumerate(readings) if rain == 0.0]

def run_q1():
    print("=" * 75)
    print("ASSIGNMENT 3 - Q1: RAINFALL RECORDS & LIST SLICING")
    print("=" * 75)

    random.seed(42)
    # Generate 365 realistic rainfall values (0 to 60 mm, with many dry 0 mm days)
    sample_year = [round(random.choice([0.0, 0.0, 0.0, 5.2, 12.0, 24.5, 45.0, 60.0]), 1) for _ in range(365)]

    # 1. Weekly totals and extremes
    w_totals = compute_weekly_totals(sample_year)
    wettest, driest = find_extreme_weeks(w_totals)
    dry_days = get_dry_days(sample_year)

    print(f"Total days analyzed: {len(sample_year)}")
    print(f"Total dry days (0 mm): {len(dry_days)}")
    print(f"Wettest Week: Week {wettest[0]} with {wettest[1]:.1f} mm")
    print(f"Driest Week : Week {driest[0]} with {driest[1]:.1f} mm")

    # Slicing explanations
    print("\n--- Slicing Semantics Explanation ---")
    print(f"readings[7:14] : Days 8 to 14 (Week 2): {sample_year[7:14]}")
    print(f"readings[-7:]  : Last 7 days of year: {sample_year[-7:]}")
    print(f"readings[::7]   : Rainfall on the first day of every week (Step 7, 53 days sampled)")

    # 2. Moving Average Verification & Edge Cases
    ma_naive = moving_average_naive(sample_year)
    ma_run = moving_average_running_sum(sample_year)
    ma_deq = moving_average_deque(sample_year)
    # Check agreement within float tolerance
    assert all(abs(a - b) < 1e-9 for a, b in zip(ma_naive, ma_run))
    assert all(abs(a - b) < 1e-9 for a, b in zip(ma_naive, ma_deq))
    print("\n[PASS] Naive, Running-sum, and Deque moving averages match exactly.")

    # Edge cases
    print(f"Empty list test           : {moving_average_running_sum([])}")
    print(f"Short list (< 7 items) test: {moving_average_running_sum([10.0, 5.0, 0.0])}")

    # 3. Experimental Investigation & Complexity Measurement
    print("\n--- Performance Investigation across Scales ---")
    print(f"{'Scale (n)':<12} | {'Naive Time (s)':<18} | {'Running-Sum Time (s)':<22} | {'Deque Time (s)':<16} | {'Speedup':<10}")
    print("-" * 85)

    scales = [365, 36_500, 365_000]
    for n in scales:
        data = [round(random.uniform(0, 50), 1) for _ in range(n)]

        t0 = time.perf_counter()
        moving_average_naive(data)
        t_naive = time.perf_counter() - t0

        t0 = time.perf_counter()
        moving_average_running_sum(data)
        t_run = time.perf_counter() - t0

        t0 = time.perf_counter()
        moving_average_deque(data)
        t_deq = time.perf_counter() - t0

        speedup = f"{t_naive / t_run:.2f}x"
        print(f"{n:<12} | {t_naive:<18.6f} | {t_run:<22.6f} | {t_deq:<16.6f} | {speedup:<10}")

    print("\n--- Theoretical Additions Derivation ---")
    print("Naive Algorithm      : Performs (window - 1) additions per window position = 6 * (n - 6) = O(window * n).")
    print("Running-Sum Algorithm: Computes initial sum (6 adds) + 1 subtraction & 1 addition per step = 6 + 2*(n - 7) = O(n).")
    print("Late Insertion Cost  : list.insert(index, val) requires shifting elements, cost O(n).")

if __name__ == "__main__":
    run_q1()
