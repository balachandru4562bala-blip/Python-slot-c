"""Main driver for Organisation D using package import."""
import os
import sys

sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
# Demonstrates both top-level package import and submodule import
import attendance_pkg
from attendance_pkg import stats
from attendance_pkg.report import generate_report

def main():
    data_file = os.path.join(os.path.dirname(__file__), "..", "..", "Task02", "day1.txt")
    records = attendance_pkg.read_attendance(data_file)
    pcts = stats.calculate_stats(records)
    streak = stats.find_consecutive_absentees(records, 3)
    print(generate_report(pcts, streak))

if __name__ == "__main__":
    main()
