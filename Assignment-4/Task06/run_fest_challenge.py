"""
ASSIGNMENT 4 - TASK 06: Fest Registration Runner
Sets up sample department files and executes the complete package pipeline.
Demonstrates resilience against bad lines, duplicates, invalid emails, and missing files.
"""

import os
import sys

CURRENT_DIR = os.path.dirname(os.path.abspath(__file__))
sys.path.insert(0, CURRENT_DIR)

from fest_registration import FestProcessor, FestReporter

def setup_test_files(data_dir):
    os.makedirs(data_dir, exist_ok=True)
    
    # 1. CS.txt: Clean records + 1 damaged line
    cs_path = os.path.join(data_dir, "CS.txt")
    with open(cs_path, "w", encoding="utf-8") as f:
        f.write("192311001,Aarav Sharma,CS,aarav@college.edu,Coding;WebDesign\n")
        f.write("192311002,Bhavana Reddy,CS,bhavana@college.edu,Hackathon;Quiz\n")
        f.write("192311003,Damaged Line Only Three Fields,CS\n")  # Damaged line
        f.write("192311004,Deepak Kumar,CS,deepak.k@gmail.com,Gaming;Coding\n")

    # 2. EC.txt: Contains duplicate of Aarav (192311001) + invalid email
    ec_path = os.path.join(data_dir, "EC.txt")
    with open(ec_path, "w", encoding="utf-8") as f:
        f.write("192311001,Aarav Sharma,EC,aarav@college.edu,Robotics\n")  # Duplicate reg_no!
        f.write("192311005,Esha Patel,EC,invalid_email_no_at.com,Robotics;Quiz\n")  # Bad email
        f.write("192311006,Farhan Akhtar,EC,farhan@college.edu,Music;Drama\n")

    # 3. ME.txt: Clean records
    me_path = os.path.join(data_dir, "ME.txt")
    with open(me_path, "w", encoding="utf-8") as f:
        f.write("192311007,Gowtham Raj,ME,gowtham@college.edu,CADModeling;Quiz\n")
        f.write("192311008,Hari Prasad,ME,hari.p@college.edu,Gaming;Robotics\n")

    # 4. EE.txt: Contains email with spaces + empty event
    ee_path = os.path.join(data_dir, "EE.txt")
    with open(ee_path, "w", encoding="utf-8") as f:
        f.write("192311009,Ishwarya M,EE,ishwarya @college.edu,Coding\n")  # Space in email
        f.write("192311010,Jeevan S,EE,jeevan@college.edu,Music;Coding\n")

    # Notice: BT.txt is DELIBERATELY NOT CREATED to demonstrate missing file resilience!

    return [
        cs_path,
        ec_path,
        me_path,
        ee_path,
        os.path.join(data_dir, "BT.txt")  # Non-existent file
    ]

def run_task06():
    print("=" * 75)
    print("ASSIGNMENT 4 - TASK 06: COLLEGE FEST REGISTRATION DESK CHALLENGE")
    print("=" * 75)

    data_dir = os.path.join(CURRENT_DIR, "data")
    output_dir = os.path.join(CURRENT_DIR, "output")
    error_log = os.path.join(output_dir, "error_log.txt")

    os.makedirs(output_dir, exist_ok=True)
    if os.path.exists(error_log):
        os.remove(error_log)

    dept_files = setup_test_files(data_dir)
    print(f"Configured 5 Department Sources (including 1 missing file).")

    # Ingest and process files
    processor = FestProcessor(error_log)
    for fpath in dept_files:
        processor.process_department_file(fpath)

    # Generate Reports
    reporter = FestReporter(output_dir)
    master_csv = reporter.write_master_csv(processor.master_records)
    event_files = reporter.write_event_files(processor.event_map)
    summary_path = reporter.write_summary_report(processor)

    # Display Results
    print(f"\nProcessing Complete with ZERO unhandled exceptions!")
    print(f"Total Lines Processed : {processor.total_lines_read}")
    print(f"Clean Records Accepted: {len(processor.master_records)}")
    print(f"Duplicates Trapped    : {processor.duplicate_count}")
    print(f"Total Rejected/Bad    : {processor.rejected_count}")

    print("\n--- Summary Report Content ---")
    with open(summary_path, "r", encoding="utf-8") as f:
        print(f.read().strip())

    print("\n--- Error Log Content ---")
    with open(error_log, "r", encoding="utf-8") as f:
        print(f.read().strip())

    print(f"\nGenerated Artifacts:")
    print(f"  Master CSV   : {os.path.basename(master_csv)}")
    print(f"  Event Lists  : {len(event_files)} event files written")
    print(f"  Summary File : {os.path.basename(summary_path)}")
    print(f"  Error Log    : {os.path.basename(error_log)}")

    assert len(processor.master_records) == 6, f"Expected 6 valid records, got {len(processor.master_records)}"
    print("\n[PASS] Task 06 Design Challenge executed successfully with full resilience.")

if __name__ == "__main__":
    run_task06()
