"""
ASSIGNMENT 4 - TASK 03: Design the Error Handling: Exceptions in Attendance Processor

Includes:
- Complete the Code: TODO 1 parse_line(), TODO 2 summarise()
- Failure taxonomy table and custom exception InvalidRecord
- Complete try-except-else-finally statement with raise ... from ...
- Misuse experiment: except Exception: pass masking typing bugs
- Handling non-existent file path
- Alternative concept: EAFP vs LBYL benchmark
"""

import os
import tempfile
import time

class InvalidRecord(Exception):
    """Raised when a line of the attendance file is not in the expected format."""

def parse_line(line):
    """'192311001,2026-10-08,P' -> ('192311001', '2026-10-08', 'P')"""
    parts = line.strip().split(",")
    # TODO 1: Raise InvalidRecord if there are not exactly 3 fields or the status is
    # not P or A; otherwise return the 3 fields as a tuple
    if len(parts) != 3:
        raise InvalidRecord(f"expected 3 fields, found {len(parts)}")
    if parts[2] not in ("P", "A"):
        raise InvalidRecord(f"invalid status '{parts[2]}'")
    return tuple(parts)

def summarise(path):
    present, absent, errors = 0, 0, []
    # TODO 2: Open the file with a with statement, parse each line inside try/except
    # InvalidRecord, count P and A, and record (line number, message) for bad lines
    try:
        with open(path, "r", encoding="utf-8") as f:
            for line_no, raw_line in enumerate(f, 1):
                line = raw_line.strip()
                if not line:
                    continue
                try:
                    reg, dt, status = parse_line(line)
                    if status == "P":
                        present += 1
                    elif status == "A":
                        absent += 1
                except InvalidRecord as e:
                    errors.append((line_no, str(e)))
    except FileNotFoundError as err:
        errors.append((0, f"File not found: {path}"))
    return present, absent, errors

# Task 3.3: Complete try-except-else-finally structure demonstration
def robust_attendance_loader(filepath):
    print("\n--- Complete try-except-else-finally Demonstration ---")
    file_handle = None
    try:
        print("1. [try]: Attempting to open file...")
        file_handle = open(filepath, "r", encoding="utf-8")
        records = [line.strip() for line in file_handle if line.strip()]
    except FileNotFoundError as e:
        print(f"2. [except FileNotFoundError]: File missing! Raising custom error...")
        raise RuntimeError("Attendance data unavailable") from e
    except PermissionError as e:
        print("2. [except PermissionError]: File locked by OS")
        raise
    else:
        print(f"3. [else]: Executed successfully! Loaded {len(records)} records.")
        return records
    finally:
        print("4. [finally]: Always executed! Ensuring clean-up...")
        if file_handle and not file_handle.closed:
            file_handle.close()
            print("   File handle closed successfully in finally block.")

# Task 3.4: Misuse Experiment
def misuse_experiment():
    print("\n--- Task 3.4: Misuse Experiment (except Exception: pass) ---")
    data = "192311001,2026-10-08,P\n"
    
    # Introduce deliberate typing bug: 'presnt_count' instead of 'present_count'
    present_count = 0
    try:
        for line in data.split("\n"):
            if not line: continue
            reg, dt, st = line.split(",")
            if st == "P":
                presnt_count += 1  # NameError: name 'presnt_count' is not defined!
    except Exception:
        pass  # Silently swallows NameError!
    
    print(f"Result with 'except Exception: pass' -> present_count = {present_count}")
    print("FATAL DEFECT: The typo NameError was silently swallowed, leaving the count as 0!")
    print("The administrator would believe zero students attended when in fact the program had a bug.")

def run_task03():
    print("=" * 75)
    print("ASSIGNMENT 4 - TASK 03: ERROR HANDLING & EXCEPTIONS")
    print("=" * 75)

    # 1. Assignment Required Execution
    print("\n--- Complete the Code Expected Execution ---")
    data = ("192311001,2026-10-08,P\n192311002,2026-10-08,A\n"
            "192311003,2026-10-08\n192311004,2026-10-08,L\n")
    with tempfile.NamedTemporaryFile("w", suffix=".csv", delete=False,
                                    encoding="utf-8") as tmp:
        tmp.write(data)
        tmp_name = tmp.name

    result = summarise(tmp_name)
    print(result)
    assert result == (1, 1, [(3, 'expected 3 fields, found 2'), (4, "invalid status 'L'")])
    os.remove(tmp_name)

    # 2. Testing non-existent file handling
    print("\n--- Non-Existent File Handling ---")
    missing_res = summarise("non_existent_file_xyz.csv")
    print("summarise('non_existent_file_xyz.csv') ->", missing_res)
    assert missing_res[2][0][0] == 0 and "File not found" in missing_res[2][0][1]

    # 3. Task 3.1: Failure Taxonomy Table
    print("\n--- Task 3.1: Exception Failure Taxonomy ---")
    failures = [
        ("Missing directory/file", "FileNotFoundError", "Verify path, log missing date, alert admin"),
        ("Locked/Read-only file", "PermissionError", "Request OS elevation, log security block"),
        ("Corrupted encoding/binary", "UnicodeDecodeError", "Fallback to utf-8-sig or latin-1, log error"),
        ("Missing fields in line", "InvalidRecord (Custom)", "Log line number and raw text to error log"),
        ("Invalid status letter", "InvalidRecord (Custom)", "Discard line, log invalid code"),
    ]
    print(f"{'Failure Scenario':<25} | {'Built-in/Custom Exception':<28} | {'Mitigation Strategy':<30}")
    print("-" * 88)
    for sc, ex, mit in failures:
        print(f"{sc:<25} | {ex:<28} | {mit:<30}")

    # 4. Run Complete try Statement & Misuse Experiment
    try:
        robust_attendance_loader("sample_dummy.txt")
    except RuntimeError as re:
        print(f"Caught top-level exception: {re}")

    misuse_experiment()

if __name__ == "__main__":
    run_task03()
