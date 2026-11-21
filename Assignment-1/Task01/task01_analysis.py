"""
TASK 01: Understand the Problem and Identify the Data
Scenario: Ksheera Village Milk Producers' Co-operative Payment System

This script demonstrates data modeling, validation rules, and complexity analysis
for processing milk collection entries.
"""

from decimal import Decimal
import sys
import time

# --- Part 1: Data Structures for Milk Collection ---
# Each entry consists of:
# farmer_id: str (e.g., "F101") - unique identifier
# litres: Decimal / float (quantity in litres, positive)
# fat: Decimal / float (percentage, valid range: 2.0 to 7.0)
# snf: Decimal / float (percentage, valid range: 6.0 to 12.0)
# shift: str ("Morning" or "Evening")

# Constants
STANDARD_FAT = Decimal("3.5")
STANDARD_SNF = Decimal("8.5")
BASE_RATE = Decimal("30.00")
FAT_STEP_VAL = Decimal("0.40")
SNF_STEP_VAL = Decimal("0.30")

MIN_FAT = Decimal("2.0")
MAX_FAT = Decimal("7.0")
MIN_SNF = Decimal("6.0")
MAX_SNF = Decimal("12.0")

def validate_entry(farmer_id, litres, fat, snf, shift):
    """
    Validates milk entry according to cooperative business rules.
    Returns (is_valid, error_message).
    """
    if not farmer_id or not isinstance(farmer_id, str):
        return False, "Farmer ID must be a non-empty string"
    if litres <= 0:
        return False, "Litres must be strictly positive"
    if not (MIN_FAT <= fat <= MAX_FAT):
        return False, f"Fat {fat}% out of valid range [{MIN_FAT}%, {MAX_FAT}%]"
    if not (MIN_SNF <= snf <= MAX_SNF):
        return False, f"SNF {snf}% out of valid range [{MIN_SNF}%, {MAX_SNF}%]"
    if shift not in ("Morning", "Evening"):
        return False, f"Invalid shift '{shift}'. Must be Morning or Evening"
    return True, "Valid"

def compute_payout(litres, fat, snf):
    """Computes rate and payout per entry."""
    fat_steps = round((fat - STANDARD_FAT) / Decimal("0.1"))
    snf_steps = round((snf - STANDARD_SNF) / Decimal("0.1"))
    rate = BASE_RATE + (fat_steps * FAT_STEP_VAL) + (snf_steps * SNF_STEP_VAL)
    amount = round(litres * rate, 2)
    return rate, amount

# --- Alternative Concept and Complexity Analysis ---
# Design A: Structured list of tuples/dictionaries: entries = [(litres, fat, snf), ...]
# Design B: 3 separate parallel scalar variables: litres1, fat1, snf1, litres2, ...
# For 300 farmers, Design B requires 900 distinct variable names, hardcoded logic,
# and cannot be looped over. Time: O(n) manual unrolled code, Space: O(n) unorganized symbols.
# Design A scales to n entries with a simple loop: Time O(n), Space O(n).

def benchmark_data_structures():
    print("=" * 60)
    print("TASK 01: DATA IDENTIFICATION & SCALABILITY DEMONSTRATION")
    print("=" * 60)
    
    # Sample validation checks
    sample_records = [
        ("F001", Decimal("15.5"), Decimal("4.2"), Decimal("8.8"), "Morning"),
        ("F002", Decimal("-5.0"), Decimal("3.5"), Decimal("8.5"), "Evening"),  # invalid litres
        ("F003", Decimal("10.0"), Decimal("1.5"), Decimal("8.5"), "Morning"),  # invalid fat
        ("F004", Decimal("12.0"), Decimal("3.5"), Decimal("13.0"), "Morning"), # invalid snf
        ("F005", Decimal("8.0"), Decimal("3.8"), Decimal("8.6"), "Night"),     # invalid shift
    ]
    
    print("\n--- Validation Test Results ---")
    for rec in sample_records:
        valid, msg = validate_entry(*rec)
        status = "PASSED" if valid else "REJECTED"
        print(f"Record {rec[0]}: {status} -> Reason: {msg}")
        if valid:
            rate, pay = compute_payout(rec[1], rec[2], rec[3])
            print(f"   Rate/L: Rs {rate:.2f} | Payout: Rs {pay:.2f}")

    # Memory and scalability demonstration for 300 farmers
    n = 300
    structured_data = [
        {"id": f"F{i:03d}", "litres": Decimal("10.0"), "fat": Decimal("4.0"), "snf": Decimal("8.5")}
        for i in range(n)
    ]
    print(f"\nMemory for structured list of {n} farmer records: {sys.getsizeof(structured_data)} bytes (container)")
    print(f"Container + element storage: approx {sys.getsizeof(structured_data) + sum(sys.getsizeof(x) for x in structured_data)} bytes")
    print("Design A (List/Tuple): O(n) time, O(n) memory, flexible, iterable.")
    print("Design B (Separate variables): Unmaintainable for 300+ farmers, lacks indexing.")

if __name__ == "__main__":
    benchmark_data_structures()
