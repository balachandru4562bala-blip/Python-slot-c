"""
Module processor.py: Coordinates file reading, error trapping, and deduplication.
"""

import os
from .validator import validate_registration_line

class FestProcessor:
    def __init__(self, error_log_path):
        self.error_log_path = error_log_path
        self.master_records = []
        self.seen_reg_nos = set()
        self.event_map = {}  # event_name -> list of records
        self.total_lines_read = 0
        self.rejected_count = 0
        self.duplicate_count = 0

    def log_error(self, filename, line_no, message, raw_text=""):
        with open(self.error_log_path, "a", encoding="utf-8") as f:
            f.write(f"[{filename}:Line {line_no}] {message} | Raw: '{raw_text}'\n")

    def process_department_file(self, file_path):
        filename = os.path.basename(file_path)
        try:
            with open(file_path, "r", encoding="utf-8") as f:
                for line_no, raw_line in enumerate(f, 1):
                    self.total_lines_read += 1
                    line = raw_line.strip()
                    if not line:
                        continue

                    ok, record, err = validate_registration_line(line)
                    if not ok:
                        self.rejected_count += 1
                        self.log_error(filename, line_no, err, line)
                        continue

                    reg_no = record["reg_no"]
                    if reg_no in self.seen_reg_nos:
                        self.duplicate_count += 1
                        self.rejected_count += 1
                        self.log_error(filename, line_no, f"Duplicate registration for {reg_no}", line)
                        continue

                    # Accepted unique record
                    self.seen_reg_nos.add(reg_no)
                    self.master_records.append(record)

                    # Accumulate into event participant mapping
                    for ev in record["events"]:
                        self.event_map.setdefault(ev, []).append(record)

        except FileNotFoundError:
            self.log_error(filename, 0, f"Department registration file missing: '{file_path}'")
        except Exception as e:
            self.log_error(filename, 0, f"Unexpected error reading file: {e}")
