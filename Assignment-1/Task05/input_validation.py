"""
TASK 05: Read Input and Convert Types
Demonstrates:
- Safe conversion of user input string to numeric types
- Handling European comma decimals ("8,5"), dirty whitespace (" 8.5 "), non-numbers ("eight")
- Aligned tabular output formatting using Python f-strings with width/precision
- Alternative concept: String pre-validation vs try-except ValueError
"""

import time

def parse_with_string_methods(text):
    """
    Validates and converts using string methods before converting.
    Handles '8,5' by replacing comma with dot.
    """
    s = text.strip().replace(",", ".")
    parts = s.split(".")
    if len(parts) == 1:
        if parts[0].isdigit():
            return float(parts[0]), True, "OK"
    elif len(parts) == 2:
        if parts[0].isdigit() and parts[1].isdigit():
            return float(s), True, "OK"
    return None, False, f"Cannot parse '{text}' with string methods"

def parse_with_try_except(text):
    """
    Validates and converts using EAFP (Easier to Ask for Forgiveness than Permission).
    Normalizes comma decimal separator.
    """
    try:
        cleaned = text.strip().replace(",", ".")
        val = float(cleaned)
        return val, True, "OK"
    except ValueError:
        return None, False, f"ValueError: invalid number '{text}'"

def format_milk_receipt(farmer_id, litres, fat, snf, rate, amount):
    """Prints a neatly aligned receipt line using f-string specifiers."""
    return f"| {farmer_id:<8} | {litres:8.2f} L | {fat:6.2f}% | {snf:6.2f}% | Rs {rate:6.2f} | Rs {amount:9.2f} |"

def run_task05_demonstrations():
    print("=" * 60)
    print("TASK 05: INPUT READING, CONVERSION & FORMATTING")
    print("=" * 60)
    
    test_inputs = [
        "8.5",
        "  8.5  ",     # whitespace
        "8,5",          # European comma decimal
        "eight",        # invalid string
        "-4.2",         # negative
        "12..4",        # multiple dots
        "0.0",          # zero
    ]
    
    print("\n--- Parsing Comparison on Typical Inputs ---")
    print(f"{'Raw Input':<12} | {'String Methods':<20} | {'Try-Except':<20}")
    print("-" * 58)
    for raw in test_inputs:
        val_str, ok_str, _ = parse_with_string_methods(raw)
        val_try, ok_try, _ = parse_with_try_except(raw)
        res_str = f"{val_str}" if ok_str else "REJECTED"
        res_try = f"{val_try}" if ok_try else "REJECTED"
        print(f"{raw:<12} | {res_str:<20} | {res_try:<20}")
        
    # Demonstrating aligned table output with f-strings
    print("\n--- Formatted Output Example ---")
    header = f"| {'ID':<8} | {'Quantity':<10} | {'Fat':<7} | {'SNF':<7} | {'Rate/L':<9} | {'Total Pay':<12} |"
    divider = "-" * len(header)
    print(divider)
    print(header)
    print(divider)
    samples = [
        ("F001", 10.0, 3.5, 8.5, 30.00, 300.00),
        ("F002", 8.5, 4.2, 8.7, 33.40, 283.90),
        ("F003", 12.0, 3.1, 8.3, 27.80, 333.60),
    ]
    for row in samples:
        print(format_milk_receipt(*row))
    print(divider)
    
    # Timing comparison for 100,000 conversions
    valid_sample = "8.5"
    iters = 100_000
    t0 = time.perf_counter()
    for _ in range(iters):
        parse_with_string_methods(valid_sample)
    t_str = time.perf_counter() - t0
    
    t0 = time.perf_counter()
    for _ in range(iters):
        parse_with_try_except(valid_sample)
    t_try = time.perf_counter() - t0
    
    print(f"\nTime for {iters} valid conversions:")
    print(f"String methods parsing : {t_str:.4f} s")
    print(f"Try-except parsing     : {t_try:.4f} s")
    print("Conclusion: try-except handles all valid floats cleanly (including negative & scientific notation)")
    print("and is the standard Pythonic idiom.")

if __name__ == "__main__":
    run_task05_demonstrations()
