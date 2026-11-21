"""
ORGANISATION A: Monolithic Single Script
Combines reading, stats, and reporting into one single script.
"""

def read_attendance(file_path):
    records = []
    with open(file_path, "r", encoding="utf-8") as f:
        for line in f:
            if line.strip():
                parts = line.strip().split(",")
                if len(parts) == 3:
                    records.append(parts)
    return records

def calculate_stats(records):
    counts = {}
    for reg, dt, st in records:
        counts.setdefault(reg, {"P": 0, "A": 0})
        if st in ("P", "A"):
            counts[reg][st] += 1
    pcts = {}
    for reg, c in counts.items():
        tot = c["P"] + c["A"]
        pcts[reg] = (c["P"] / tot * 100.0) if tot > 0 else 0.0
    return pcts

def find_consecutive_absentees(records, consecutive_days=3):
    """Changed Requirement: 3 consecutive absences."""
    # Group dates by student
    student_records = {}
    for reg, dt, st in sorted(records, key=lambda x: (x[0], x[1])):
        student_records.setdefault(reg, []).append((dt, st))
    
    flagged = []
    for reg, history in student_records.items():
        streak = 0
        for dt, st in history:
            if st == "A":
                streak += 1
                if streak >= consecutive_days:
                    flagged.append(reg)
                    break
            else:
                streak = 0
    return sorted(list(set(flagged)))

def generate_report(pcts, consecutive_absentees=None):
    lines = ["--- Attendance Report ---"]
    for reg, pct in sorted(pcts.items()):
        status = "ELIGIBLE" if pct >= 75.0 else "SHORTAGE (< 75%)"
        lines.append(f"{reg}: {pct:.1f}% ({status})")
    if consecutive_absentees:
        lines.append("\n--- Students Absent for 3 Consecutive Days ---")
        for reg in consecutive_absentees:
            lines.append(f"FLAGGED: {reg}")
    return "\n".join(lines)

if __name__ == "__main__":
    import os
    data_file = os.path.join(os.path.dirname(__file__), "..", "Task02", "day1.txt")
    recs = read_attendance(data_file)
    pcts = calculate_stats(recs)
    abs_streak = find_consecutive_absentees(recs, 3)
    print(generate_report(pcts, abs_streak))
