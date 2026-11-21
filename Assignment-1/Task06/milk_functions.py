"""
TASK 06: Organise the Logic into Functions
Demonstrates:
- Modular decomposition: rate_per_litre(), payout(), ten_day_total()
- Return values vs printing side-effects
- Local vs global scope and immutability of configuration constants
- Complete PEP 257 docstrings
- Alternative concept: Monolithic script vs Lambda expressions vs Named functions
- Function call overhead measurement
"""

import time

# Named constants in global scope
BASE_RATE = 30.00
STANDARD_FAT = 3.5
STANDARD_SNF = 8.5
FAT_STEP_VAL = 0.40
SNF_STEP_VAL = 0.30

def rate_per_litre(fat: float, snf: float) -> float:
    """
    Computes the price per litre based on fat and SNF percentages.

    Parameters:
        fat (float): Percentage of milk fat (e.g., 4.2).
        snf (float): Percentage of solids-not-fat (e.g., 8.7).

    Returns:
        float: Rate in Rupees per litre rounded to 2 decimal places.
    """
    fat_steps = round((fat - STANDARD_FAT) / 0.1)
    snf_steps = round((snf - STANDARD_SNF) / 0.1)
    rate = BASE_RATE + (fat_steps * FAT_STEP_VAL) + (snf_steps * SNF_STEP_VAL)
    return round(rate, 2)

def payout(litres: float, fat: float, snf: float) -> float:
    """
    Computes total payout for a single milk collection entry.

    Parameters:
        litres (float): Quantity of milk in litres.
        fat (float): Fat percentage.
        snf (float): SNF percentage.

    Returns:
        float: Net payout amount in Rupees rounded to 2 decimal places.
    """
    rate = rate_per_litre(fat, snf)
    return round(litres * rate, 2)

def ten_day_total(entries: list) -> float:
    """
    Aggregates payouts for a 10-day payment cycle (typically 20 shifts).

    Parameters:
        entries (list of tuple): List of (litres, fat, snf) measurements.

    Returns:
        float: Sum of all payouts rounded to 2 decimal places.
    """
    total = 0.0
    for litres, fat, snf in entries:
        total += payout(litres, fat, snf)
    return round(total, 2)

# --- Scope Demonstration ---
def scope_demonstration():
    """Shows difference between reading global constants and local scoping."""
    local_bonus = 5.00
    # Reading global BASE_RATE is permitted
    effective_base = BASE_RATE + local_bonus
    # Modifying global without 'global' keyword raises UnboundLocalError if attempted:
    # BASE_RATE += 1  <-- UnboundLocalError
    return effective_base

# --- Alternative Concept: Lambda Expressions ---
lambda_rate = lambda f, s: round(BASE_RATE + round((f - STANDARD_FAT) / 0.1) * FAT_STEP_VAL + round((s - STANDARD_SNF) / 0.1) * SNF_STEP_VAL, 2)
lambda_payout = lambda l, f, s: round(l * lambda_rate(f, s), 2)

def run_task06_demonstrations():
    print("=" * 60)
    print("TASK 06: FUNCTIONAL DECOMPOSITION & SCOPE")
    print("=" * 60)
    
    # 1. Ten-day payment calculation for a sample farmer
    # 2 shifts per day for 5 sample days = 10 entries
    farmer_entries = [
        (10.0, 3.5, 8.5),  # standard: 300.00
        (8.5, 4.2, 8.7),   # 33.40 * 8.5 = 283.90
        (12.0, 3.1, 8.3),  # 27.80 * 12 = 333.60
        (9.0, 3.6, 8.6),   # 30.70 * 9 = 276.30
        (11.0, 4.0, 8.5),  # 32.00 * 11 = 352.00
        (10.5, 3.5, 8.4),  # 29.70 * 10.5 = 311.85
        (7.5, 4.5, 9.0),   # 35.50 * 7.5 = 266.25
        (10.0, 3.8, 8.6),  # 31.50 * 10 = 315.00
        (12.5, 3.4, 8.5),  # 29.60 * 12.5 = 370.00
        (8.0, 4.1, 8.8),   # 33.30 * 8 = 266.40
    ]
    
    total = ten_day_total(farmer_entries)
    print(f"Computed 10-day total for 10 shifts: Rs {total:.2f}")
    print(f"Scope demonstration output: effective base = Rs {scope_demonstration():.2f}")
    
    # 2. Performance comparison: Named functions vs Lambdas vs Monolithic inline
    n_runs = 100_000
    
    # Named function
    t0 = time.perf_counter()
    for _ in range(n_runs):
        payout(10.0, 4.2, 8.7)
    t_func = time.perf_counter() - t0
    
    # Lambda
    t0 = time.perf_counter()
    for _ in range(n_runs):
        lambda_payout(10.0, 4.2, 8.7)
    t_lambda = time.perf_counter() - t0
    
    # Monolithic inline (no function calls)
    t0 = time.perf_counter()
    for _ in range(n_runs):
        r = round(30.00 + round((4.2 - 3.5) / 0.1) * 0.40 + round((8.7 - 8.5) / 0.1) * 0.30, 2)
        p = round(10.0 * r, 2)
    t_inline = time.perf_counter() - t0
    
    print(f"\nTime for {n_runs} evaluations:")
    print(f"Named functions : {t_func:.4f} s")
    print(f"Lambda functions: {t_lambda:.4f} s")
    print(f"Monolithic inline: {t_inline:.4f} s")
    print("\nAnalysis: Function call overhead in Python is minimal (approx nanoseconds per call)")
    print("while modularity, testability, and docstrings provide immense software engineering benefits.")

if __name__ == "__main__":
    run_task06_demonstrations()
