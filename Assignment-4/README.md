# Assignment 4: File Handling, Exceptions, Modules and Packages

**Course Outcome**: CO4 — Design and implement Python programs using file handling, modules, and packages to process and analyse data effectively  
**Bloom's Levels**: K3 Apply, K4 Analyse, K5 Evaluate  
**Total Marks**: 50  

---

## 1. Assignment Objectives
- Diagnose file-processing scripts for memory bloat, descriptor leaks, and swallowed exceptions.
- Implement robust I/O pipelines with context managers (`with`), streaming generators, and exact decimal arithmetic.
- Construct specialized custom exceptions (`InvalidRecord`) and implement the full `try-except-else-finally` lifecycle.
- Conduct software forensics on file overwriting and newline omission bugs.
- Architect applications across four standard Python structural paradigms (monolith, single module, multi-module, package).
- Design and execute a complete cultural fest registration package resilient to missing files, duplicates, and malformed inputs.

---

## 2. Directory Structure

```
Assignment-4/
├── Task01/
│   ├── mess_oct.txt                      # Sample hostel mess data with defects
│   └── mess_bills_diagnostic.py          # Defect diagnosis and repaired streaming processor
├── Task02/
│   ├── BIOMETRIC_ATTENDANCE_SPEC.md      # Data model, pseudocode, and trace table
│   └── attendance_design.py              # Biometric monthly attendance pipeline prototype
├── Task03/
│   └── attendance_exceptions.py          # Complete the Code TODO 1 & 2, custom exception, try/else/finally
├── Task04/
│   └── file_forensics.py                 # File forensics on overwrites, missing newlines, audit logger
├── Task05/
│   ├── org_a_monolith/                   # (a) Single script monolith
│   ├── org_b_single_module/              # (b) Single module + main driver
│   ├── org_c_three_modules/              # (c) Three decoupled modules
│   ├── org_d_package/                    # (d) Structured package with __init__.py
│   └── run_four_organisations.py         # Comparative execution, requirement change & import semantics
├── Task06/
│   ├── FEST_DESIGN_SPEC.md               # 5-stage architectural specification
│   ├── fest_registration/                # Robust modular package (validator, processor, reporter)
│   ├── data/                             # Department registration data files
│   ├── output/                           # Generated clean master CSV, event lists, summary & error log
│   └── run_fest_challenge.py             # Design challenge runner and test suite
├── test_results.txt                      # Verified test execution log
├── requirements.txt                      # Python dependencies
└── README.md                             # Assignment documentation
```

---

## 3. Description of Tasks and Implementations

### Task 01: File-Processing Design Review (Hostel Mess Bills)
- **File**: `Task01/mess_bills_diagnostic.py`
- **Key Findings**: Identifies 7 fatal deficiencies in the naive script (hardcoded paths, unclosed files, $O(\text{file size})$ memory buffer, bare `except: pass`, `int()` truncation on paise, $O(n^2)$ string concatenation, no error tracking). Rewrites into an $O(1)$ memory streaming pipeline using `with` and `Decimal`.

### Task 02: Biometric Attendance Processing Design
- **Files**: `Task02/BIOMETRIC_ATTENDANCE_SPEC.md`, `Task02/attendance_design.py`
- **Key Findings**: Models daily biometric files into student presence/absence counts. Implements streaming reads, writes monthly percentage summary and defaulters list ($< 75\%$), and appends damaged lines to an error log.

### Task 03: Exception Handling in Attendance Processor
- **File**: `Task03/attendance_exceptions.py`
- **Key Findings**: Completes TODO 1 (`parse_line`) and TODO 2 (`summarise`) using custom `InvalidRecord` exception. Demonstrates complete `try-except-else-finally` with `raise ... from ...` chaining and proves in Task 3.4 that `except Exception: pass` silently masks naming typos.

### Task 04: File and Exception Forensics (Library Book Returns)
- **File**: `Task04/file_forensics.py`
- **Key Findings**: Uncovers why earlier days were lost (mode `'w'` instead of `'a'`) and why book titles merged together (missing `\n`). Fixes program with context managers, newline delimiters, and an error audit log.

### Task 05: Code Organisation Four Ways
- **Files**: `Task05/run_four_organisations.py`, `org_a_monolith/`, `org_b_single_module/`, `org_c_three_modules/`, `org_d_package/`
- **Key Findings**: Organises utility into 4 architectures. Adds a 3-consecutive-day absence report and evaluates file change impacts. Compares readability, reuse, unit testing, and namespace safety.

### Task 06: Design Challenge (College Fest Registration Desk)
- **Files**: `Task06/FEST_DESIGN_SPEC.md`, `Task06/run_fest_challenge.py`, `fest_registration/`
- **Key Findings**: Full 5-stage engineering response. Processes registrations from 5 departments. Eliminates duplicates with sets in $O(n)$ time, validates emails using string methods (no regex), logs damaged lines, gracefully absorbs missing department files, and produces all required output files with zero unhandled exceptions.

---

## 4. Execution Commands

```bash
# Task 01: Mess Bills Review
python Assignment-4/Task01/mess_bills_diagnostic.py

# Task 02: Attendance Pipeline Prototype
python Assignment-4/Task02/attendance_design.py

# Task 03: Attendance Exceptions
python Assignment-4/Task03/attendance_exceptions.py

# Task 04: File Forensics
python Assignment-4/Task04/file_forensics.py

# Task 05: Four Organisations Comparison
python Assignment-4/Task05/run_four_organisations.py

# Task 06: College Fest Challenge
python Assignment-4/Task06/run_fest_challenge.py
```
