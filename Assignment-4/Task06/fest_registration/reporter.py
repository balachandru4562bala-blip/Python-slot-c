"""
Module reporter.py: Generates clean master CSV, event files, and summary report.
"""

import os
import csv

class FestReporter:
    def __init__(self, output_dir):
        self.output_dir = output_dir
        os.makedirs(self.output_dir, exist_ok=True)

    def write_master_csv(self, master_records):
        csv_path = os.path.join(self.output_dir, "clean_master_list.csv")
        fieldnames = ["RegisterNo", "Name", "Department", "Email", "EventsCount", "EventsList"]
        with open(csv_path, "w", newline="", encoding="utf-8") as f:
            writer = csv.DictWriter(f, fieldnames=fieldnames)
            writer.writeheader()
            for r in master_records:
                writer.writerow({
                    "RegisterNo": r["reg_no"],
                    "Name": r["name"],
                    "Department": r["department"],
                    "Email": r["email"],
                    "EventsCount": len(r["events"]),
                    "EventsList": "; ".join(r["events"])
                })
        return csv_path

    def write_event_files(self, event_map):
        created_files = []
        for event_name, participants in event_map.items():
            # Sanitize event name for filename
            clean_name = "".join(c if c.isalnum() else "_" for c in event_name)
            filename = f"event_{clean_name}.txt"
            filepath = os.path.join(self.output_dir, filename)

            # Sort participants alphabetically by name
            sorted_participants = sorted(participants, key=lambda x: x["name"])

            with open(filepath, "w", encoding="utf-8") as f:
                f.write(f"=== PARTICIPANT LIST: {event_name.upper()} ===\n")
                f.write(f"Total Participants: {len(sorted_participants)}\n\n")
                f.write(f"{'Name':<25} | {'Reg No':<12} | {'Department':<12} | {'Email':<30}\n")
                f.write("-" * 85 + "\n")
                for p in sorted_participants:
                    f.write(f"{p['name']:<25} | {p['reg_no']:<12} | {p['department']:<12} | {p['email']:<30}\n")
            created_files.append(filepath)
        return created_files

    def write_summary_report(self, processor):
        summary_path = os.path.join(self.output_dir, "summary_report.txt")
        with open(summary_path, "w", encoding="utf-8") as f:
            f.write("=====================================================\n")
            f.write("COLLEGE CULTURAL FEST: REGISTRATION DESK SUMMARY\n")
            f.write("=====================================================\n\n")
            f.write(f"Total Raw Lines Processed : {processor.total_lines_read}\n")
            f.write(f"Valid Registrations Accepted: {len(processor.master_records)}\n")
            f.write(f"Duplicate Registrations   : {processor.duplicate_count}\n")
            f.write(f"Total Rejected/Bad Lines  : {processor.rejected_count}\n\n")
            f.write("--- Event-Wise Enrollment Counts ---\n")
            for ev, plist in sorted(processor.event_map.items(), key=lambda x: -len(x[1])):
                f.write(f"  {ev:<20}: {len(plist):3d} students\n")
        return summary_path
