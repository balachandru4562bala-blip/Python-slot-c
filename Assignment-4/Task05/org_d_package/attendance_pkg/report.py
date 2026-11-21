"""Package attendance_pkg: report.py"""
def generate_report(pcts, consecutive_absentees=None):
    lines = ["--- Attendance Report (Organisation D - Package) ---"]
    for reg, pct in sorted(pcts.items()):
        status = "ELIGIBLE" if pct >= 75.0 else "SHORTAGE (< 75%)"
        lines.append(f"{reg}: {pct:.1f}% ({status})")
    if consecutive_absentees:
        lines.append("\n--- Students Absent for 3 Consecutive Days ---")
        for reg in consecutive_absentees:
            lines.append(f"FLAGGED: {reg}")
    return "\n".join(lines)
