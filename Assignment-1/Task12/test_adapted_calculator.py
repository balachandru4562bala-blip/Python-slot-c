"""
TASK 12: Comprehensive Validation of Adapted Calculator
Tests:
- 2-decimal high-precision inputs (e.g. 4.25% fat, 8.63% snf)
- Summer Season rates (May) vs Regular Season rates (October)
- Volume bonus boundary checks (499.9L, 500.0L, 500.1L)
"""

from decimal import Decimal
from adapted_calculator import (
    calculate_rate_adapted,
    calculate_entry_payout,
    calculate_ten_day_bill
)

def run_tests():
    print("=" * 70)
    print("TASK 12: VALIDATION OF ADAPTED CO-OPERATIVE CALCULATOR")
    print("=" * 70)

    # 1. High-precision 2-decimal fat and SNF testing
    # Input: Fat = 4.25%, SNF = 8.63%
    # Summer Season (May, month=5):
    # Fat diff: 4.25 - 3.5 = 0.75 -> (0.75/0.1) = 7.5 steps -> rounded to 8 steps
    # SNF diff: 8.63 - 8.5 = 0.13 -> (0.13/0.1) = 1.3 steps -> rounded to 1 step
    # Rate = 32.00 + (8 * 0.45 = 3.60) + (1 * 0.30 = 0.30) = Rs 35.90
    rate_summer = calculate_rate_adapted(Decimal("4.25"), Decimal("8.63"), month=5)
    print(f"Summer (May) Rate for 4.25% fat, 8.63% snf: Rs {rate_summer} (Expected: 35.90)")
    assert rate_summer == Decimal("35.90"), f"Expected 35.90, got {rate_summer}"

    # Regular Season (October, month=10):
    # Base: 30.00, Fat step: 0.40, SNF step: 0.30
    # Rate = 30.00 + (8 * 0.40 = 3.20) + (1 * 0.30 = 0.30) = Rs 33.50
    rate_reg = calculate_rate_adapted(Decimal("4.25"), Decimal("8.63"), month=10)
    print(f"Regular (Oct) Rate for 4.25% fat, 8.63% snf: Rs {rate_reg} (Expected: 33.50)")
    assert rate_reg == Decimal("33.50"), f"Expected 33.50, got {rate_reg}"

    # 2. Volume Bonus Boundary Verification
    print("\n--- Volume Bonus Boundary Verification ---")

    # Boundary 1: 499.9 Litres (Below 500) -> NO BONUS
    entries_499 = [(Decimal("49.99"), Decimal("3.5"), Decimal("8.5")) for _ in range(10)]
    bill_499 = calculate_ten_day_bill(entries_499, month=10)
    print(f"Test 499.9L: Total Litres = {bill_499['total_litres']}, Bonus = Rs {bill_499['bonus_amount']}")
    assert bill_499['bonus_amount'] == Decimal("0.00")
    assert bill_499['qualifies_bonus'] is False

    # Boundary 2: Exactly 500.0 Litres -> NO BONUS (Rule: strictly greater than 500)
    entries_500 = [(Decimal("50.0"), Decimal("3.5"), Decimal("8.5")) for _ in range(10)]
    bill_500 = calculate_ten_day_bill(entries_500, month=10)
    print(f"Test 500.0L: Total Litres = {bill_500['total_litres']}, Bonus = Rs {bill_500['bonus_amount']}")
    assert bill_500['bonus_amount'] == Decimal("0.00")
    assert bill_500['qualifies_bonus'] is False

    # Boundary 3: 500.1 Litres -> QUALIFIES FOR BONUS on ALL litres (500.1 * 0.50 = Rs 250.05)
    entries_501 = [(Decimal("50.01"), Decimal("3.5"), Decimal("8.5")) for _ in range(10)]
    bill_501 = calculate_ten_day_bill(entries_501, month=10)
    expected_bonus = (bill_501['total_litres'] * Decimal("0.50")).quantize(Decimal("0.01"))
    print(f"Test 500.1L: Total Litres = {bill_501['total_litres']}, Bonus = Rs {bill_501['bonus_amount']}")
    assert bill_501['qualifies_bonus'] is True
    assert bill_501['bonus_amount'] == expected_bonus
    assert bill_501['final_total'] == bill_501['base_payout'] + expected_bonus

    print("\n" + "=" * 70)
    print("ALL ADAPTED DESIGN CHALLENGE TESTS PASSED!")
    print("=" * 70)

if __name__ == "__main__":
    run_tests()
