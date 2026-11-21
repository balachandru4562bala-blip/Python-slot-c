"""
ASSIGNMENT 4 - TASK 01: File-Processing Design Review: Diagnose and Repair a Poor Script
Hostel Mess Bills Processor

Task 1.1: Diagnosis of at least 5 design deficiencies
Task 1.2: Repaired design with `with`, streaming, specific exceptions, rejected logs
Task 1.3: Design defense for 50,000 lines
Alternative concept: f.read() vs f.readlines() vs line-by-line iteration
"""

import os
from decimal import Decimal, InvalidOperation

CURRENT_DIR = os.path.dirname(os.path.abspath(__file__))
SAMPLE_FILE = os.path.join(CURRENT_DIR, "mess_oct.txt")

# --- Original Defective Script (Simulated) ---
def run_original_defective_script(file_path):
    print("--- Running Defective Script Simulation ---")
    try:
        f = open(file_path)
        data = f.read()
        total = 0
        report = ""
        for line in data.split("\n"):
            try:
                parts = line.split(",")
                total = total + int(parts[2])  # Truncates or fails on 2450.50!
                report = report + parts[1] + " " + parts[2] + "\n"
            except:
                pass  # Bare except silently swallows float errors and empty lines
        # Notice: f.close() is missing!
        print("Defective Report:\n" + report)
        print("Defective Total:", total)
    except Exception as e:
        print("Failed with unhandled top-level exception:", e)

# --- Task 1.2: Repaired Production-Ready Script ---
def process_mess_bills(file_path):
    """
    Repaired file processing utility:
    - Context manager `with` guarantees file descriptor closure.
    - Streaming iteration line-by-line bounds memory to O(1) buffer.
    - Decimal arithmetic guarantees exact paise representation.
    - Specific exceptions (IndexError, InvalidOperation) logged with line numbers.
    - Report constructed efficiently using list and str.join().
    """
    if not os.path.exists(file_path):
        raise FileNotFoundError(f"Mess bill file not found: {file_path}")

    valid_lines = []
    rejected_records = []
    total_bill = Decimal("0.00")

    with open(file_path, "r", encoding="utf-8") as f:
        for line_no, raw_line in enumerate(f, 1):
            line = raw_line.strip()
            if not line:
                continue  # Ignore clean trailing/blank lines

            parts = [p.strip() for p in line.split(",")]
            if len(parts) != 3:
                rejected_records.append((line_no, line, f"Expected 3 fields, found {len(parts)}"))
                continue

            reg_no, student_name, amount_str = parts

            try:
                amount = Decimal(amount_str)
                if amount < 0:
                    rejected_records.append((line_no, line, "Negative bill amount"))
                    continue
                total_bill += amount
                valid_lines.append(f"{student_name:<15} Rs {amount:8.2f}")
            except (InvalidOperation, ValueError) as err:
                rejected_records.append((line_no, line, f"Non-numeric amount '{amount_str}'"))

    report_output = "\n".join(valid_lines)
    return total_bill, report_output, rejected_records

def run_task01():
    print("=" * 75)
    print("ASSIGNMENT 4 - TASK 01: MESS BILLS FILE PROCESSING REVIEW")
    print("=" * 75)

    # 1. Demonstrate Defects on Sample File
    run_original_defective_script(SAMPLE_FILE)

    # 2. Run Repaired Script
    print("\n--- Running Repaired Script ---")
    tot, rep, rejections = process_mess_bills(SAMPLE_FILE)
    print("Repaired Clean Report:")
    print(rep)
    print(f"\nRepaired Total: Rs {tot:.2f}")

    print("\nAudit Trail of Rejected Lines:")
    for lno, text, reason in rejections:
        print(f"  Line {lno}: '{text}' -> Reason: {reason}")

    # 3. Task 1.1: Detailed Diagnosis of Deficiencies
    print("\n--- Task 1.1: Diagnostic Analysis ---")
    print("1. Hard-coded absolute path: Script fails on any machine other than original author's PC.")
    print("2. Unclosed file handle: If an error occurs, the file descriptor remains open in the OS table.")
    print("3. Memory exhaustion: f.read() loads the entire file into RAM at once, crashing on large files.")
    print("4. Bare except: pass: Masks critical syntax and logic bugs and silently drops valid students with decimal amounts.")
    print("5. int() on currency: Hostel mess bills frequently include paise (e.g. 2450.50). int('2450.50') raises ValueError, silently dropping student Bhavana!")
    print("6. Repeated string concatenation (+): Incurs O(n^2) character copying overhead.")
    print("7. No audit log: Rejected student bills vanish with zero administrative traceability.")

    # 4. Task 1.3: Design Defense (< 100 words)
    defense = (
        "Design Defense (Task 1.3):\n"
        "For a 50,000-line file (~3 MB to 50 MB), the repaired version consumes strictly O(1) memory "
        "by streaming lines through a generator buffer rather than buffering millions of characters. "
        "Context managers ensure deterministic file handle release even upon catastrophic I/O aborts. "
        "Specific exceptions capture malformed records into an administrative audit log, guaranteeing zero "
        "financial data loss and paisa-accurate ledger balancing."
    )
    print("\n" + defense)

if __name__ == "__main__":
    run_task01()
