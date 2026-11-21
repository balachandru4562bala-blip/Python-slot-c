"""
TASK 04: Write Correct Expressions
Demonstrates:
- Operator precedence and associativity
- Binary floating-point nuances: (4.2 - 3.5) / 0.1
- Difference between round(), int(), and math.floor() on positive and negative values
- Comparison chaining and Boolean logic
- Demonstration of 3 surprising expressions
- Alternative concept analysis: truncation vs floor vs round
"""

import math

def compute_steps_round(current, standard):
    """Accurate step calculation using round()."""
    return round((current - standard) / 0.1)

def compute_steps_int(current, standard):
    """Step calculation using int() truncation (rounds towards zero)."""
    return int((current - standard) / 0.1)

def compute_steps_floor(current, standard):
    """Step calculation using math.floor() (rounds towards -infinity)."""
    return math.floor((current - standard) / 0.1)

def run_task04_demonstrations():
    print("=" * 60)
    print("TASK 04: CORRECT MATHEMATICAL EXPRESSIONS & SURPRISES")
    print("=" * 60)
    
    # 1. Floating-point division surprise
    raw_step = (4.2 - 3.5) / 0.1
    print(f"(4.2 - 3.5) / 0.1 raw result : {raw_step}")
    print(f"Fixed with round(..., 0)     : {round(raw_step)}")
    print(f"Truncated with int()         : {int(raw_step)}")
    print(f"Floored with math.floor()    : {math.floor(raw_step)}")
    
    # 2. Three Surprising Expressions in Python
    print("\n--- Three Surprising Expressions Explained ---")
    
    # Surprise 1: Unary minus and exponentiation precedence
    # -3 ** 2 is evaluated as -(3 ** 2) = -9, NOT (-3) ** 2 = 9
    s1 = -3 ** 2
    print(f"Surprise 1: -3 ** 2 = {s1}")
    print("   Explanation: ** has higher precedence than unary -, so -(3**2) = -9.")
    
    # Surprise 2: Floating point associativity
    # (0.1 + 0.2) + 0.3 != 0.1 + (0.2 + 0.3)
    s2_left = (0.1 + 0.2) + 0.3
    s2_right = 0.1 + (0.2 + 0.3)
    print(f"Surprise 2: (0.1 + 0.2) + 0.3 == 0.1 + (0.2 + 0.3) -> {s2_left == s2_right}")
    print(f"   Left:  {s2_left}")
    print(f"   Right: {s2_right}")
    print("   Explanation: Binary floating point additions accumulate rounding errors non-associatively.")
    
    # Surprise 3: Banker's Rounding (round-half-to-even)
    r2_5 = round(2.5)
    r3_5 = round(3.5)
    print(f"Surprise 3: round(2.5) = {r2_5}, round(3.5) = {r3_5}")
    print("   Explanation: Python uses Banker's rounding: .5 rounds to nearest EVEN number.")
    
    # 3. Negative value behavior comparison: fat = 3.1 (below standard 3.5)
    print("\n--- Negative Step Analysis for fat = 3.1 and fat = 4.2 ---")
    test_cases = [4.2, 3.1]
    for f in test_cases:
        diff_div = (f - 3.5) / 0.1
        st_round = compute_steps_round(f, 3.5)
        st_int = compute_steps_int(f, 3.5)
        st_floor = compute_steps_floor(f, 3.5)
        print(f"\nFat = {f}%:")
        print(f"   (f - 3.5) / 0.1 raw  : {diff_div}")
        print(f"   round() steps       : {st_round} -> Rate: Rs {30.0 + st_round * 0.40:.2f}")
        print(f"   int() steps         : {st_int} -> Rate: Rs {30.0 + st_int * 0.40:.2f}")
        print(f"   math.floor() steps  : {st_floor} -> Rate: Rs {30.0 + st_floor * 0.40:.2f}")

    # 4. Chained comparisons
    sample_fat = 4.5
    valid_range = 2.0 <= sample_fat <= 7.0
    print(f"\nChained comparison (2.0 <= {sample_fat} <= 7.0): {valid_range}")
    print("Time complexity of each expression: O(1); Space: O(1).")

if __name__ == "__main__":
    run_task04_demonstrations()
