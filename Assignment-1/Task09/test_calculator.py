"""
TASK 09: Test Suite for Milk Calculator
Tests all boundary conditions, normal records, invalid inputs, and hand-calculated cases.
"""

from decimal import Decimal
import time
from milk_calculator import (
    calculate_rate,
    calculate_payment,
    validate_milk_record,
    process_batch
)

def run_tests():
    print("=" * 60)
    print("TASK 09: EXECUTING AUTOMATED CALCULATOR VALIDATION TESTS")
    print("=" * 60)

    # 1. Normal Cases (both directions)
    # (a) Standard: 3.5% Fat, 8.5% SNF -> Rate: Rs 30.00
    r_std = calculate_rate(Decimal("3.5"), Decimal("8.5"))
    assert r_std == Decimal("30.00"), f"Expected 30.00, got {r_std}"
    print("[PASS] Normal Case 1: Standard (3.5% fat, 8.5% snf) -> Rs 30.00")

    # (b) Above standard: 4.2% Fat (+7 steps), 8.7% SNF (+2 steps)
    # 30.00 + (7 * 0.40 = 2.80) + (2 * 0.30 = 0.60) = Rs 33.40
    r_above = calculate_rate(Decimal("4.2"), Decimal("8.7"))
    assert r_above == Decimal("33.40"), f"Expected 33.40, got {r_above}"
    p_above = calculate_payment(Decimal("8.5"), r_above) # 8.5 * 33.40 = 283.90
    assert p_above == Decimal("283.90"), f"Expected 283.90, got {p_above}"
    print("[PASS] Normal Case 2: Above Standard (4.2% fat, 8.7% snf) -> Rate 33.40, Pay 283.90")

    # (c) Below standard: 3.1% Fat (-4 steps), 8.3% SNF (-2 steps)
    # 30.00 - (4 * 0.40 = 1.60) - (2 * 0.30 = 0.60) = Rs 27.80
    r_below = calculate_rate(Decimal("3.1"), Decimal("8.3"))
    assert r_below == Decimal("27.80"), f"Expected 27.80, got {r_below}"
    p_below = calculate_payment(Decimal("12.0"), r_below) # 12.0 * 27.80 = 333.60
    assert p_below == Decimal("333.60"), f"Expected 333.60, got {p_below}"
    print("[PASS] Normal Case 3: Below Standard (3.1% fat, 8.3% snf) -> Rate 27.80, Pay 333.60")

    # 2. Boundary Cases
    # (a) Lowest allowed fat: 2.0% Fat (-15 steps) -> 30.00 - 6.00 = Rs 24.00
    r_min_fat = calculate_rate(Decimal("2.0"), Decimal("8.5"))
    assert r_min_fat == Decimal("24.00"), f"Expected 24.00, got {r_min_fat}"
    print("[PASS] Boundary Case 1: Minimum Fat (2.0%) -> Rs 24.00")

    # (b) Highest allowed fat: 7.0% Fat (+35 steps) -> 30.00 + 14.00 = Rs 44.00
    r_max_fat = calculate_rate(Decimal("7.0"), Decimal("8.5"))
    assert r_max_fat == Decimal("44.00"), f"Expected 44.00, got {r_max_fat}"
    print("[PASS] Boundary Case 2: Maximum Fat (7.0%) -> Rs 44.00")

    # (c) Boundary SNF: Min 6.0% (-25 steps = -7.50) -> Rs 22.50
    r_min_snf = calculate_rate(Decimal("3.5"), Decimal("6.0"))
    assert r_min_snf == Decimal("22.50"), f"Expected 22.50, got {r_min_snf}"
    print("[PASS] Boundary Case 3: Minimum SNF (6.0%) -> Rs 22.50")

    # 3. Invalid Cases Validation
    invalid_cases = [
        ("F01", "eight", "3.5", "8.5", "Morning"),     # text quantity
        ("F02", "-5.0", "3.5", "8.5", "Evening"),      # negative quantity
        ("F03", "10.0", "1.9", "8.5", "Morning"),      # fat below min (1.9 < 2.0)
        ("F04", "10.0", "7.1", "8.5", "Morning"),      # fat above max (7.1 > 7.0)
        ("F05", "10.0", "3.5", "5.9", "Morning"),      # snf below min (5.9 < 6.0)
        ("F06", "10.0", "3.5", "8.5", "Afternoon"),    # invalid shift
    ]
    for raw in invalid_cases:
        ok, err = validate_milk_record(*raw)
        assert not ok, f"Expected validation failure for {raw}, got pass"
        print(f"[PASS] Rejected Invalid Entry: {raw[0]} ({raw[1]}, {raw[2]}, {raw[3]}, {raw[4]}) -> {err}")

    # 4. Hand-calculated 5-Entry Benchmark
    print("\n--- Hand-Calculated 5-Entry Batch Test ---")
    five_entries = [
        ("F001", "10.0", "3.5", "8.5", "Morning"), # Rate: 30.00, Pay: 300.00
        ("F002", "15.0", "4.0", "8.5", "Evening"), # Rate: 32.00, Pay: 480.00
        ("F003", "8.0",  "3.0", "8.5", "Morning"), # Rate: 28.00, Pay: 224.00
        ("F004", "12.5", "3.8", "8.8", "Evening"), # Rate: 30 + 1.20 + 0.90 = 32.10, Pay: 12.5 * 32.10 = 401.25
        ("F005", "20.0", "3.2", "8.2", "Morning"), # Rate: 30 - 1.20 - 0.90 = 27.90, Pay: 20 * 27.90 = 558.00
    ]
    # Expected grand total = 300.00 + 480.00 + 224.00 + 401.25 + 558.00 = Rs 1963.25
    batch_res = process_batch(five_entries)
    print(f"Processed Valid Records: {len(batch_res['valid'])} / {len(five_entries)}")
    print(f"Batch Total Litres     : {batch_res['total_litres']} L")
    print(f"Batch Total Payout     : Rs {batch_res['total_payout']}")
    assert batch_res['total_payout'] == Decimal("1963.25"), f"Expected 1963.25, got {batch_res['total_payout']}"
    print("[PASS] Hand-Calculated 5-Entry Total Matches Exact Bank Expectation (Rs 1963.25)")

    # 5. Timing comparison: Automated asserts vs Manual testing
    t0 = time.perf_counter()
    for _ in range(1000):
        process_batch(five_entries)
    t_auto = (time.perf_counter() - t0) / 1000
    print(f"\nAutomated test execution time per run: {t_auto * 1000:.3f} ms")
    print("Manual typing test time: ~60 to 120 seconds per run with high human error risk.")
    print("=" * 60)
    print("ALL TESTS PASSED SUCCESSFULLY!")
    print("=" * 60)

if __name__ == "__main__":
    run_tests()
