"""
ASSIGNMENT 4 - TASK 02: Biometric Attendance Processing Prototype
Executes the data model, processing flow, and report generation designed in BIOMETRIC_ATTENDANCE_SPEC.md
"""

import os
import csv
from collections import defaultdict

CURRENT_DIR = os.path.dirname(os.path.abspath(__file__))

def process_daily_attendance_file(file_path, accumulator, error_log_path):
    """Parses a single biometric attendance file and accumulates counts."""
    filename = os.path.basename(file_path)
    with open(file_path, "r", encoding="utf-8") as f, open(error_log_path, "a", encoding="utf-8") as err_log:
        for line_no, raw_line in enumerate(f, 1):
            line = raw_line.strip()
            if not line:
                continue

            parts = [p.strip() for p in line.split(",")]
            if len(parts) != 3:
                err_log.write(f"[{filename}:{line_no}] Damaged line (expected 3 fields): '{line}'\n")
                continue

            reg_no, dt, status = parts
            if status not in ("P", "A"):
                err_log.write(f"[{filename}:{line_no}] Invalid status '{status}' in line: '{line}'\n")
                continue

            accumulator[reg_no][status] += 1

def generate_reports(accumulator, summary_csv, defaulters_csv):
    """Writes monthly summary and shortage reports."""
    summary_rows = []
    defaulters_rows = []

    for reg_no, counts in sorted(accumulator.items()):
        p = counts["P"]
        a = counts["A"]
        total = p + a
        pct = (p / total * 100.0) if total > 0 else 0.0

        summary_rows.append({
            "RegisterNo": reg_no,
            "Present": p,
            "Absent": a,
            "TotalDays": total,
            "Percentage": f"{pct:.2f}%"
        })

        if pct < 75.0:
            defaulters_rows.append({
                "RegisterNo": reg_no,
                "AttendancePercentage": f"{pct:.2f}%",
                "Status": "Exam Hall Ticket Withheld (< 75%)"
            })

    # Write summary CSV
    with open(summary_csv, "w", newline="", encoding="utf-8") as f:
        writer = csv.DictWriter(f, fieldnames=["RegisterNo", "Present", "Absent", "TotalDays", "Percentage"])
        writer.writeheader()
        writer.writerows(summary_rows)

    # Write defaulters CSV
    with open(defaulters_csv, "w", newline="", encoding="utf-8") as f:
        writer = csv.DictWriter(f, fieldnames=["RegisterNo", "AttendancePercentage", "Status"])
        writer.writeheader()
        writer.writerows(defaulters_rows)

    return summary_rows, defaulters_rows

def run_task02():
    print("=" * 75)
    print("ASSIGNMENT 4 - TASK 02: BIOMETRIC ATTENDANCE PROCESSING PROTOTYPE")
    print("=" * 75)

    # Create dummy days data
    sample_day1 = os.path.join(CURRENT_DIR, "day1.txt")
    sample_day2 = os.path.join(CURRENT_DIR, "day2.txt")
    err_log = os.path.join(CURRENT_DIR, "damaged_records.log")
    summary_csv = os.path.join(CURRENT_DIR, "monthly_summary.csv")
    defaulters_csv = os.path.join(CURRENT_DIR, "defaulters_below_75.csv")

    with open(sample_day1, "w", encoding="utf-8") as f:
        f.write("192311001,2026-10-01,P\n192311002,2026-10-01,A\n192311003,2026-10-01\n192311004,2026-10-01,L\n")
    with open(sample_day2, "w", encoding="utf-8") as f:
        f.write("192311001,2026-10-02,P\n192311002,2026-10-02,P\n192311004,2026-10-02,A\n")

    # Clear previous log
    if os.path.exists(err_log):
        os.remove(err_log)

    accumulator = defaultdict(lambda: {"P": 0, "A": 0})
    process_daily_attendance_file(sample_day1, accumulator, err_log)
    process_daily_attendance_file(sample_day2, accumulator, err_log)

    summary, defaulters = generate_reports(accumulator, summary_csv, defaulters_csv)

    print("\n--- Summary Report Output ---")
    for r in summary:
        print(r)

    print("\n--- Defaulters Report (< 75%) ---")
    for r in defaulters:
        print(r)

    print("\n--- Damaged Records Log Content ---")
    with open(err_log, "r", encoding="utf-8") as f:
        print(f.read().strip())

    print("\n[PASS] Task 02 end-to-end file pipeline executed successfully.")

if __name__ == "__main__":
    run_task02()
