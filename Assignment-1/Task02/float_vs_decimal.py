"""
TASK 02: Explore Values and Types in the Interpreter
Includes:
- Complete the Code: TODO 1 (exact decimal summation)
- Float vs Decimal comparison
- Effect of Decimal(float(amount))
- Integer paise alternative
- Division operators (/, //, %, -//) and binary floating point behavior
"""

from decimal import Decimal
import sys
import time

# 1,000 payments of Rs 33.40 and three small adjustments of Rs 0.10
payments = ["33.40"] * 1000 + ["0.10"] * 3

def total_float(items):
    total = 0.0
    for amount in items:
        total += float(amount)
    return total

def total_decimal(items):
    # TODO 1: Add the amounts exactly by creating a Decimal from each string, and
    # return the Decimal total
    total = Decimal("0.0")
    for amount in items:
        total += Decimal(amount)
    return total

def total_decimal_from_float(items):
    """Demonstrates loss of precision when converting string -> float -> Decimal."""
    total = Decimal("0.0")
    for amount in items:
        total += Decimal(float(amount))
    return total

def total_paise(items):
    """Alternative concept: represent currency in integer paise (1 Rupee = 100 Paise)."""
    total_paise_val = 0
    for amount in items:
        # Convert string to integer paise without float error
        rupees, paise = amount.split(".")
        total_paise_val += int(rupees) * 100 + int(paise)
    return total_paise_val / 100

def run_task02_demonstrations():
    print("=" * 60)
    print("TASK 02: VALUES AND TYPES EXPLORATION")
    print("=" * 60)
    
    # 1. Assignment required output
    print("float  :", total_float(payments))
    print("Decimal:", total_decimal(payments))
    print(0.1 + 0.2 == 0.3, Decimal("0.1") + Decimal("0.2") == Decimal("0.3"))
    
    print("\n--- Decimal(float(amount)) Result ---")
    print("Decimal from float:", total_decimal_from_float(payments))
    print("Explanation: float('33.40') has IEEE 754 binary approximation error.")
    print("Passing float to Decimal constructor preserves that binary error!")
    
    print("\n--- Division Operators Exploration ---")
    print(f"7 / 2   = {7 / 2} (float true division)")
    print(f"7 // 2  = {7 // 2} (integer floor division)")
    print(f"7 % 2   = {7 % 2} (modulus / remainder)")
    print(f"-7 // 2 = {-7 // 2} (floors towards negative infinity, not zero)")
    
    print("\n--- Alternative Concept: Integer Paise vs Decimal ---")
    print(f"Integer paise total (in Rupees): {total_paise(payments):.2f}")
    
    # Memory comparison with sys.getsizeof
    f_val = 33.40
    d_val = Decimal("33.40")
    i_val = 3340
    print(f"\nMemory used per value:")
    print(f"float (33.40)         : {sys.getsizeof(f_val)} bytes")
    print(f"Decimal ('33.40')     : {sys.getsizeof(d_val)} bytes")
    print(f"int paise (3340)      : {sys.getsizeof(i_val)} bytes")

if __name__ == "__main__":
    run_task02_demonstrations()
