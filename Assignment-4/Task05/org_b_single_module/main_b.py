"""Main driver for Organisation B."""
import os
import sys

sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
import attendance_lib

def main():
    data_file = os.path.join(os.path.dirname(__file__), "..", "..", "Task02", "day1.txt")
    records = attendance_lib.read_attendance(data_file)
    pcts = attendance_lib.calculate_stats(records)
    streak = attendance_lib.find_consecutive_absentees(records, 3)
    print(attendance_lib.generate_report(pcts, streak))

if __name__ == "__main__":
    main()
