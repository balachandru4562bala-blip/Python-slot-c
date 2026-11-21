"""Organisation C: main_c.py"""
import os
import sys

sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
import reader
import stats
import report

def main():
    data_file = os.path.join(os.path.dirname(__file__), "..", "..", "Task02", "day1.txt")
    records = reader.read_attendance(data_file)
    pcts = stats.calculate_stats(records)
    streak = stats.find_consecutive_absentees(records, 3)
    print(report.generate_report(pcts, streak))

if __name__ == "__main__":
    main()
