"""Package attendance_pkg: reader.py"""
def read_attendance(file_path):
    records = []
    with open(file_path, "r", encoding="utf-8") as f:
        for line in f:
            if line.strip():
                parts = line.strip().split(",")
                if len(parts) == 3:
                    records.append(parts)
    return records
