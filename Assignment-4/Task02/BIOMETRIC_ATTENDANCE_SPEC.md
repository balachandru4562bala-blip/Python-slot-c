# ASSIGNMENT 4 - TASK 02: BIOMETRIC ATTENDANCE FILE PROCESSING DESIGN SPECIFICATION

---

## Task 2.1: Data Modeling
1. **Input File Format**:
   - Filename convention: `attendance_YYYY-MM-DD.txt` (e.g., `attendance_2026-10-01.txt`).
   - Line schema: `register_no,date,status`
   - Example: `192311001,2026-10-08,P`
   - Constraints: `status` must be either `'P'` (Present) or `'A'` (Absent).
2. **In-Memory Accumulator Data Structures**:
   - `attendance_counts = defaultdict(lambda: {'P': 0, 'A': 0})`
   - Maps student register number to total counts of presence and absence.
3. **Output Files**:
   - `monthly_summary.csv`: `RegisterNo,PresentCount,AbsentCount,TotalDays,Percentage`
   - `defaulters_below_75.csv`: `RegisterNo,AttendancePercentage,EligibleForExam`
   - `damaged_records.log`: Audit log recording `Timestamp,Filename,LineNumber,RawText,ErrorMessage`

---

## Task 2.2: Design of File Operations
- **Input Mode (`r`, encoding='utf-8')**: Stream-oriented line iteration `for line in f:` to conserve memory.
- **Summary Reports (`w`, newline='', encoding='utf-8')**: Overwrites final aggregated reports at the conclusion of monthly batch processing.
- **Damaged Record Log (`a`, encoding='utf-8')**: Appends error entries immediately to preserve persistent diagnostic history across runs.

---

## Task 2.3: SIMATS-Compliant Algorithmic Pseudocode
```text
ALGORITHM ProcessMonthlyBiometricAttendance(folder_path, output_dir)
START
    SET attendance_data TO empty dictionary
    SET error_log_path TO output_dir + "/damaged_records.log"
    SET daily_files TO LIST_FILES(folder_path, pattern="*.txt")

    FOR each file_path IN daily_files DO
        OPEN file_path IN READ MODE WITH utf-8 encoding AS f DO
            SET line_number TO 0
            FOR each raw_line IN f DO
                SET line_number TO line_number + 1
                SET line TO TRIM(raw_line)
                IF line IS EMPTY THEN
                    CONTINUE
                ENDIF

                SET parts TO SPLIT(line, ",")
                IF LENGTH(parts) != 3 THEN
                    LOG_ERROR(error_log_path, file_path, line_number, line, "Expected 3 fields")
                    CONTINUE
                ENDIF

                SET reg_no TO parts[0]
                SET date_val TO parts[1]
                SET status TO parts[2]

                IF status != "P" AND status != "A" THEN
                    LOG_ERROR(error_log_path, file_path, line_number, line, "Invalid status " + status)
                    CONTINUE
                ENDIF

                // Update Accumulator
                IF reg_no NOT IN attendance_data THEN
                    SET attendance_data[reg_no] TO {'P': 0, 'A': 0}
                ENDIF
                SET attendance_data[reg_no][status] TO attendance_data[reg_no][status] + 1
            ENDFOR
        CLOSE f
    ENDFOR

    // Generate Reports
    GENERATE_SUMMARY_REPORT(attendance_data, output_dir + "/monthly_summary.csv")
    GENERATE_DEFAULTERS_REPORT(attendance_data, output_dir + "/defaulters_below_75.csv", threshold=75.0)
END
```

---

## Task 2.4: Hand Trace for Sample File with Damaged Lines

### Input File `sample_day.txt`:
```
Line 1: 192311001,2026-10-08,P
Line 2: 192311002,2026-10-08,A
Line 3: 192311003,2026-10-08
Line 4: 192311004,2026-10-08,L
```

| Line | Line Content | Fields Count | Status Check | Action Taken | State of `attendance_data` | Log Entry |
|---|---|---|---|---|---|---|
| 1 | `192311001,2026-10-08,P` | 3 | 'P' (Valid) | Accumulate P | `{'192311001': {'P': 1, 'A': 0}}` | None |
| 2 | `192311002,2026-10-08,A` | 3 | 'A' (Valid) | Accumulate A | `{'192311001': {'P': 1, 'A': 0}, '192311002': {'P': 0, 'A': 1}}` | None |
| 3 | `192311003,2026-10-08` | 2 | Missing | Log Error | Unchanged | Line 3: Expected 3 fields |
| 4 | `192311004,2026-10-08,L` | 3 | 'L' (Invalid) | Log Error | Unchanged | Line 4: Invalid status 'L' |
