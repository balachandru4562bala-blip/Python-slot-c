"""
ASSIGNMENT 4 - TASK 04: File and Exception Forensics
Library Returned Books Logging System

Includes:
- Task 4.1: Defect identification
- Task 4.2: Concrete evidence construction running defective program for 3 days
- Task 4.3: Repaired program using append mode, newlines, with statements, error logging
- Task 4.4: Prevention rules
- Alternative concept: Manual try/finally vs with context manager
"""

import os

CURRENT_DIR = os.path.dirname(os.path.abspath(__file__))

# --- Original Defective Implementation ---
def save_returns_defective(books, log_path):
    log = open(log_path, "w")  # DEFECT 1: "w" overwrites previous entries!
    for b in books:
        log.write(b)           # DEFECT 2: Missing newline '\n', strings run together!
    log.close()                # DEFECT 3: Not safe against unhandled write failures!

def process_defective(day_file, log_path):
    try:
        books = open(day_file).read().split("\n")  # Unclosed file handle
        save_returns_defective(books, log_path)
    except FileNotFoundError:
        print("missing")

# --- Task 4.3: Repaired Implementation ---
def save_returns_repaired(books, log_path):
    """
    Repaired logger:
    - Mode 'a' preserves historic returns.
    - Each book title appended on its own line with '\n'.
    - Context manager ensures clean descriptor close.
    """
    with open(log_path, "a", encoding="utf-8") as log:
        for b in books:
            clean_b = b.strip()
            if clean_b:
                log.write(clean_b + "\n")

def process_repaired(day_file, log_path, error_log_path):
    """
    Robust daily return processor with structured error logging.
    """
    try:
        with open(day_file, "r", encoding="utf-8") as f:
            books = [line.strip() for line in f if line.strip()]
        save_returns_repaired(books, log_path)
    except FileNotFoundError as e:
        with open(error_log_path, "a", encoding="utf-8") as err_log:
            err_log.write(f"ERROR: Missing daily file '{day_file}': {e}\n")
    except Exception as e:
        with open(error_log_path, "a", encoding="utf-8") as err_log:
            err_log.write(f"UNEXPECTED ERROR processing '{day_file}': {e}\n")

def run_task04():
    print("=" * 75)
    print("ASSIGNMENT 4 - TASK 04: FILE AND EXCEPTION FORENSICS")
    print("=" * 75)

    # Create 3 daily return files
    d1_file = os.path.join(CURRENT_DIR, "day1_books.txt")
    d2_file = os.path.join(CURRENT_DIR, "day2_books.txt")
    d3_file = os.path.join(CURRENT_DIR, "day3_books.txt")

    with open(d1_file, "w") as f: f.write("Python Programming\nData Structures\n")
    with open(d2_file, "w") as f: f.write("Operating Systems\nComputer Networks\n")
    with open(d3_file, "w") as f: f.write("Database Systems\nCompiler Design\n")

    # 1. Task 4.2: Construct Evidence of Defects
    defective_log = os.path.join(CURRENT_DIR, "returns_defective.log")
    if os.path.exists(defective_log): os.remove(defective_log)

    print("\n--- Running Defective Process across 3 Days ---")
    process_defective(d1_file, defective_log)
    process_defective(d2_file, defective_log)
    process_defective(d3_file, defective_log)

    print("Defective returns.log Content:")
    with open(defective_log, "r") as f:
        content = f.read()
    print(repr(content))
    print(content)
    print("Forensic Findings:")
    print("1. Days 1 and 2 books ('Python Programming', 'Operating Systems', etc.) are COMPLETELY GONE!")
    print("2. Day 3 books are merged together without spacing: 'Database SystemsCompiler Design'")

    # 2. Task 4.3: Run Repaired Implementation
    repaired_log = os.path.join(CURRENT_DIR, "returns_repaired.log")
    error_log = os.path.join(CURRENT_DIR, "library_errors.log")
    if os.path.exists(repaired_log): os.remove(repaired_log)
    if os.path.exists(error_log): os.remove(error_log)

    print("\n--- Running Repaired Process across 3 Days (including missing day) ---")
    process_repaired(d1_file, repaired_log, error_log)
    process_repaired(d2_file, repaired_log, error_log)
    process_repaired(os.path.join(CURRENT_DIR, "day_missing.txt"), repaired_log, error_log)
    process_repaired(d3_file, repaired_log, error_log)

    print("Repaired returns.log Content:")
    with open(repaired_log, "r") as f:
        repaired_content = f.read()
    print(repaired_content)

    print("Repaired error.log Content:")
    with open(error_log, "r") as f:
        print(f.read().strip())

    # 3. Task 4.4: Prevention Rules
    print("\n--- Task 4.4: Rules to Prevent Recurrence ---")
    print("Rule 1: ALWAYS access files using the `with` statement context manager to guarantee deterministic closure.")
    print("Rule 2: For cumulative logs or ledgers, ALWAYS open in append mode ('a') with explicit newline delimiters ('\\n').")

if __name__ == "__main__":
    run_task04()
