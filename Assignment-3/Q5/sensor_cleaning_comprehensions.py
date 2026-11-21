"""
ASSIGNMENT 3 - Q5: List Comprehension: Cleaning Sensor Readings
Cold-Storage Vaccine Temperature Monitor

Features:
- Filtering invalid readings (< -50 C or > 50 C)
- Converting valid Celsius readings to Fahrenheit: F = (C * 9/5) + 32
- Alarm detection: Temperature outside safe storage band [2.0 C, 8.0 C]
- 4 Implementations:
  1. Standard for loop with .append()
  2. List comprehension with condition
  3. map() and filter() with lambda
  4. Alarm minutes using enumerate()
- Dictionary and Set Comprehension examples
- Memory profiling: List comprehension vs Generator expression (sys.getsizeof)
- Benchmark across 10,000, 100,000, and 1,000,000 readings
"""

import time
import sys
import random

# Implementation 1: For loop with append
def clean_for_loop(readings):
    cleaned_f = []
    for c in readings:
        if -50.0 <= c <= 50.0:
            f = (c * 9.0 / 5.0) + 32.0
            cleaned_f.append(round(f, 2))
    return cleaned_f

# Implementation 2: List Comprehension with condition
def clean_list_comprehension(readings):
    return [round((c * 9.0 / 5.0) + 32.0, 2) for c in readings if -50.0 <= c <= 50.0]

# Implementation 3: map() and filter() with lambda
def clean_map_filter(readings):
    valid = filter(lambda c: -50.0 <= c <= 50.0, readings)
    converted = map(lambda c: round((c * 9.0 / 5.0) + 32.0, 2), valid)
    return list(converted)

# Implementation 4: Alarm minutes detection using enumerate()
def detect_alarm_minutes(readings):
    """Detects minutes where VALID temperature was outside [2.0 C, 8.0 C]."""
    alarms = []
    for minute, temp in enumerate(readings):
        if -50.0 <= temp <= 50.0:  # Valid reading
            if temp < 2.0 or temp > 8.0:
                alarms.append((minute, temp))
    return alarms

# Dict and Set Comprehensions
def demo_dict_and_set_comprehensions(readings):
    # Dict: Minute -> Valid Celsius
    valid_dict = {minute: temp for minute, temp in enumerate(readings) if -50.0 <= temp <= 50.0}
    # Set: Unique rounded valid temperatures
    unique_temps = {round(temp, 1) for temp in readings if -50.0 <= temp <= 50.0}
    return valid_dict, unique_temps

def run_q5():
    print("=" * 75)
    print("ASSIGNMENT 3 - Q5: SENSOR CLEANING & LIST COMPREHENSIONS")
    print("=" * 75)

    # 1. Verification of Small Sample Data
    sample_data = [4.2, 5.1, 8.5, -60.0, 3.8, 105.0, 1.9, 6.0, -50.0, 50.0]
    res_loop = clean_for_loop(sample_data)
    res_comp = clean_list_comprehension(sample_data)
    res_map = clean_map_filter(sample_data)
    alarms = detect_alarm_minutes(sample_data)

    print(f"Raw readings: {sample_data}")
    print(f"Cleaned (For Loop)     : {res_loop}")
    print(f"Cleaned (Comprehension): {res_comp}")
    print(f"Cleaned (Map-Filter)   : {res_map}")
    print(f"Alarm Minutes (out of 2-8 C range): {alarms}")

    assert res_loop == res_comp == res_map
    print("[PASS] All 3 cleaning implementations produce identical results.")

    # 2. Memory Comparison: List Comprehension vs Generator Expression
    print("\n--- Memory: List Comprehension vs Generator Expression ---")
    n_sample = 500_000
    test_temps = [random.uniform(-60, 60) for _ in range(n_sample)]

    comp_list = [c for c in test_temps if -50 <= c <= 50]
    gen_expr = (c for c in test_temps if -50 <= c <= 50)

    mem_list = sys.getsizeof(comp_list)
    mem_gen = sys.getsizeof(gen_expr)

    print(f"Size of materialized list ({len(comp_list)} elements): {mem_list} bytes ({mem_list / (1024*1024):.2f} MB)")
    print(f"Size of generator object                                : {mem_gen} bytes (Constant O(1) memory!)")
    print(f"Memory reduction factor: {mem_list / mem_gen:.0f}x")

    # 3. Performance Benchmark across Scales
    print("\n--- Execution Time across Scales ---")
    print(f"{'Readings':<12} | {'For Loop (s)':<16} | {'Comprehension (s)':<20} | {'Map-Filter (s)':<18} | {'Speedup Comp vs Loop':<22}")
    print("-" * 90)

    scales = [10_000, 100_000, 1_000_000]
    for n in scales:
        dataset = [random.uniform(-60, 60) for _ in range(n)]

        t0 = time.perf_counter()
        _ = clean_for_loop(dataset)
        t_loop = time.perf_counter() - t0

        t0 = time.perf_counter()
        _ = clean_list_comprehension(dataset)
        t_comp = time.perf_counter() - t0

        t0 = time.perf_counter()
        _ = clean_map_filter(dataset)
        t_mf = time.perf_counter() - t0

        speedup = f"{t_loop / t_comp:.2f}x"
        print(f"{n:<12} | {t_loop:<16.6f} | {t_comp:<20.6f} | {t_mf:<18.6f} | {speedup:<22}")

    print("\n--- Conclusion ---")
    print("List comprehensions are consistently ~20-30% faster than standard for-loops due to C-level bytecode optimization (LIST_APPEND).")
    print("However, when only summary aggregation is needed (e.g. sum, min, max), generator expressions should be preferred to preserve memory.")

if __name__ == "__main__":
    run_q5()
