"""
TASK 03: Choose Variables and Name the Constants
Demonstrates:
- PEP 8 named constants
- Why Python lacks true constants and uses naming conventions
- Dynamic typing and variable re-binding
- Multiple assignment and swapping
- Alternative concept: Magic numbers vs Dictionary RATE_CARD
"""

import sys
import time

# --- Named Constants (Single Point of Truth) ---
BASE_RATE = 30.00         # Base rate in Rs per litre
STANDARD_FAT = 3.5        # Benchmark Fat percentage
STANDARD_SNF = 8.5        # Benchmark SNF percentage
FAT_STEP_VALUE = 0.40     # Rs added/deducted per 0.1% fat
SNF_STEP_VALUE = 0.30     # Rs added/deducted per 0.1% SNF

MIN_FAT_LIMIT = 2.0       # Minimum acceptable fat percentage
MAX_FAT_LIMIT = 7.0       # Maximum acceptable fat percentage
MIN_SNF_LIMIT = 6.0       # Minimum acceptable SNF percentage
MAX_SNF_LIMIT = 12.0      # Maximum acceptable SNF percentage

# --- Alternative Concept: Dictionary Rate Card ---
RATE_CARD = {
    "base_rate": 30.00,
    "standard_fat": 3.5,
    "standard_snf": 8.5,
    "fat_step_val": 0.40,
    "snf_step_val": 0.30,
    "min_fat": 2.0,
    "max_fat": 7.0,
}

def calculate_rate_constants(fat, snf):
    fat_steps = round((fat - STANDARD_FAT) / 0.1)
    snf_steps = round((snf - STANDARD_SNF) / 0.1)
    return round(BASE_RATE + (fat_steps * FAT_STEP_VALUE) + (snf_steps * SNF_STEP_VALUE), 2)

def calculate_rate_dict(fat, snf, rate_card):
    fat_steps = round((fat - rate_card["standard_fat"]) / 0.1)
    snf_steps = round((snf - rate_card["standard_snf"]) / 0.1)
    return round(rate_card["base_rate"] + (fat_steps * rate_card["fat_step_val"]) + (snf_steps * rate_card["snf_step_val"]), 2)

def calculate_rate_magic_numbers(fat, snf):
    # Fragile: Magic numbers embedded in expression
    return round(30.00 + (round((fat - 3.5) / 0.1) * 0.40) + (round((snf - 8.5) / 0.1) * 0.30), 2)

def run_task03_demonstrations():
    print("=" * 60)
    print("TASK 03: CONSTANTS, VARIABLES, AND DYNAMIC TYPING")
    print("=" * 60)
    
    # 1. Dynamic typing demonstration
    sample_var = 100
    print(f"Initial: sample_var = {sample_var}, type = {type(sample_var)}")
    sample_var = "One Hundred"
    print(f"Reassigned: sample_var = {sample_var}, type = {type(sample_var)}")
    
    # 2. Multiple assignment and swapping
    shift_morning = "Shift-1"
    shift_evening = "Shift-2"
    print(f"\nBefore swap: Morning = {shift_morning}, Evening = {shift_evening}")
    shift_morning, shift_evening = shift_evening, shift_morning
    print(f"After swap:  Morning = {shift_morning}, Evening = {shift_evening}")
    
    # 3. Rate calculation comparison
    test_fat, test_snf = 4.2, 8.7
    r1 = calculate_rate_constants(test_fat, test_snf)
    r2 = calculate_rate_dict(test_fat, test_snf, RATE_CARD)
    r3 = calculate_rate_magic_numbers(test_fat, test_snf)
    print(f"\nRate for fat={test_fat}%, snf={test_snf}%:")
    print(f"Using Named Constants : Rs {r1:.2f}")
    print(f"Using Dictionary Card : Rs {r2:.2f}")
    print(f"Using Magic Numbers   : Rs {r3:.2f}")
    
    # 4. Performance & Memory Comparison
    print(f"\nMemory of RATE_CARD dictionary: {sys.getsizeof(RATE_CARD)} bytes")
    
    iters = 100_000
    t0 = time.perf_counter()
    for _ in range(iters):
        calculate_rate_constants(4.0, 8.5)
    t_const = time.perf_counter() - t0
    
    t0 = time.perf_counter()
    for _ in range(iters):
        calculate_rate_dict(4.0, 8.5, RATE_CARD)
    t_dict = time.perf_counter() - t0
    
    print(f"Time for {iters} calls using Constants: {t_const:.4f} s")
    print(f"Time for {iters} calls using Dictionary: {t_dict:.4f} s")
    print("Conclusion: Constants offer direct variable access (faster) and maintainability.")
    print("Magic numbers require editing k expressions across code, prone to partial updates.")

if __name__ == "__main__":
    run_task03_demonstrations()
