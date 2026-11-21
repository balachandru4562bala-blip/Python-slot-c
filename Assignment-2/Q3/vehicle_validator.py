"""
ASSIGNMENT 2 - Q3: Engineer a Vehicle Registration Number Validator
Toll Plaza Number-Plate Records

Includes:
- Complete the Code: TODO 1 normalise(), TODO 2 is_valid()
- Formatting receipt string: format_receipt()
- Explanations of string immutability, upper(), and negative slicing s[-4:], s[4:-4]
- Alternative concept: Regular expression (re.fullmatch) vs Slicing & String methods
"""

import re
import time

def normalise(text):
    """'tn 09 ab 1234' -> 'TN09AB1234' (spaces and hyphens removed, upper case)."""
    # TODO 1: Remove spaces and hyphens and convert to upper case using string methods
    return text.replace(" ", "").replace("-", "").upper()

def is_valid(reg):
    """Valid form: 2 letters, 2 digits, 1 or 2 letters, 4 digits (e.g. TN09AB1234)."""
    # TODO 2: Check the length is 9 or 10, then check each part using slicing with
    # isalpha() and isdigit()
    if len(reg) not in (9, 10):
        return False
    state = reg[0:2]
    district = reg[2:4]
    series = reg[4:-4]
    number = reg[-4:]
    return state.isalpha() and district.isdigit() and series.isalpha() and number.isdigit()

def format_receipt(reg):
    """Formats normalised valid plate for receipt: 'TN 09 AB 1234' or 'KA 01 M 0007'."""
    if not is_valid(reg):
        return "INVALID"
    state = reg[0:2]
    district = reg[2:4]
    series = reg[4:-4]
    number = reg[-4:]
    return f"{state} {district} {series} {number}"

# Alternative Concept: Regular Expressions
REG_PATTERN = re.compile(r"^[A-Z]{2}[0-9]{2}[A-Z]{1,2}[0-9]{4}$")

def is_valid_regex(reg):
    return bool(REG_PATTERN.fullmatch(reg))

def run_q3():
    print("=" * 70)
    print("ASSIGNMENT 2 - Q3: VEHICLE REGISTRATION VALIDATOR")
    print("=" * 70)

    # 1. Assignment Required Execution
    print("\n--- Assignment Expected Execution ---")
    raw_samples = ["tn 09 ab 1234", "KA-01-M-0007", "TN9AB1234", "TN 22 1234 AB"]
    for raw in raw_samples:
        reg = normalise(raw)
        print(f"{raw:15} -> {reg:11} {'valid' if is_valid(reg) else 'INVALID'}")

    # 2. Receipt Formatting Demonstration
    print("\n--- Receipt Formatted Outputs ---")
    receipt_samples = ["tn 09 ab 1234", "KA-01-M-0007", "dl-01-c-9999", "mh 12 5555"]
    for raw in receipt_samples:
        n = normalise(raw)
        v = is_valid(n)
        fmt = format_receipt(n)
        print(f"{raw:16} -> Normalised: {n:11} | Valid: {str(v):<5} | Receipt: '{fmt}'")

    # 3. Inquiry Explanations
    print("\n--- Conceptual Inquiry & Explanations ---")
    print("1. String Immutability: In Python, `str` objects cannot be modified in-place.")
    print("   Any operation like `replace()` or `upper()` constructs and returns a NEW string object in memory.")
    print("2. Why `text.upper()` doesn't modify `text`: `text` continues pointing to the original memory buffer.")
    print("3. Negative Slicing Behavior:")
    s9 = "KA01M0007"   # 9 characters
    s10 = "TN09AB1234"  # 10 characters
    print(f"   9-char  '{s9}':  s[-4:] = '{s9[-4:]}' (last 4 digits), s[4:-4] = '{s9[4:-4]}' (1-letter series)")
    print(f"   10-char '{s10}': s[-4:] = '{s10[-4:]}' (last 4 digits), s[4:-4] = '{s10[4:-4]}' (2-letter series)")

    # 4. Performance Comparison: Slicing vs Regex
    iters = 100_000
    test_str = "TN09AB1234"
    t0 = time.perf_counter()
    for _ in range(iters):
        is_valid(test_str)
    t_slice = time.perf_counter() - t0

    t0 = time.perf_counter()
    for _ in range(iters):
        is_valid_regex(test_str)
    t_re = time.perf_counter() - t0

    print(f"\nTime for {iters} validations:")
    print(f"String slicing & methods : {t_slice:.4f} s")
    print(f"Compiled Regular Expression: {t_re:.4f} s")
    print("Slicing is faster and teaches elementary indexing fundamentals without external libraries.")

if __name__ == "__main__":
    run_q3()
