"""Organisation C: stats.py"""
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
