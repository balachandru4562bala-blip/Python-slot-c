# Python Programming Comprehensive Lab Assignments (CO1 – CO5)

**Course**: CSA08 – Python Programming  
**Curriculum Scope**: Units I through V (CO1 to CO5)  
**Academic Institution**: SIMATS Engineering – Online Lab & Project Submission  
**Python Runtime**: Python 3.12+ (Tested on Python 3.14.7 x64 Windows Environment)  

---

## 1. Master Repository Overview

This repository contains the complete, verified, academic implementation of all **five** Python Programming assignments for Course CSA08. Every task, question, design challenge, and "Complete the Code" section has been authored from first principles, tested with strict assertions, verified against reference outputs, and accompanied by comprehensive documentation.

```
Python-Programming-Assignments/
│
├── Assignment-1/               # CO1: Milk Co-operative Payment Calculator (Tasks 01 to 12)
│   ├── Task01/ to Task12/      # Complete source code, models, and design challenge
│   ├── test_results.txt        # Verified execution outputs
│   ├── requirements.txt        # Python standard library dependencies
│   └── README.md               # Assignment 1 documentation
│
├── Assignment-2/               # CO2: Control Flow and String Operations (Q1 to Q7)
│   ├── Q1/ to Q7/              # Branching, loops, string mechanics, recursion, and DP redesign
│   ├── test_results.txt        # Verified execution outputs
│   ├── requirements.txt        # Python standard library dependencies
│   └── README.md               # Assignment 2 documentation
│
├── Assignment-3/               # CO3: Python Data Structures (Q1 to Q7)
│   ├── Q1/ to Q7/              # Lists, tuples, dicts, sets, comprehensions, and entity resolution
│   ├── test_results.txt        # Verified execution outputs
│   ├── requirements.txt        # Python standard library dependencies
│   └── README.md               # Assignment 3 documentation
│
├── Assignment-4/               # CO4: File Handling, Exceptions, Modules & Packages (Tasks 01 to 06)
│   ├── Task01/ to Task06/      # Script diagnostics, streaming, custom exceptions, fest package
│   ├── test_results.txt        # Verified execution outputs
│   ├── requirements.txt        # Python standard library dependencies
│   └── README.md               # Assignment 4 documentation
│
├── Assignment-5/               # CO5: Data Acquisition, Visualisation, and AI Applications
│   ├── Part-A/ (A1 to A5)      # Algorithmic pseudocode & engineering design specifications
│   ├── Part-B/ (B1 to B4)      # Cleaning pipeline, adversarial tests, SQL benchmarks, text AI
│   ├── data/                   # Data directory
│   ├── database/               # air_quality.db (SQLite database with B-Tree indices)
│   ├── charts/                 # Generated Matplotlib publication-quality charts (PNG)
│   ├── test_results.txt        # Verified execution outputs
│   ├── requirements.txt        # External dependencies (pandas, matplotlib)
│   └── README.md               # Assignment 5 documentation
│
└── README.md                   # Master repository documentation (This file)
```

---

## 2. Course Outcomes and Technical Highlights

### Assignment 1: Payment Calculator for a Village Milk Co-operative (CO1)
- **Key Focus**: Numeric representations, floating point precision pitfalls, financial calculations with `decimal.Decimal`, single point of truth constants, algorithmic pseudocode, and modular functions.
- **Complete the Code**: `Task02/float_vs_decimal.py` (`total_decimal()`) and `Task07/milkrate.py` (`rate_per_litre()`, `payout()`).
- **Design Challenge (Task 12)**: Adapts payment engine for 2-decimal high-precision analyser readings (4.25% Fat, 8.63% SNF), April–June seasonal rates (Rs 32.00 base, Rs 0.45 fat step), and retrospective volume bonuses ($> 500$ L earns Rs 0.50/L on all litres).

### Assignment 2: Control Flow and String Operations (CO2)
- **Key Focus**: Branch evaluation and boundaries (`if-elif-else`), loop lifecycle (`break`, `continue`, `pass`, loop `else`), string immutability, parameter default binding lifetimes (`__defaults__`), and recursion stack boundaries.
- **Complete the Code**:
  - `Q3/vehicle_validator.py`: `normalise()`, `is_valid()` (No regex, string slicing only).
  - `Q4/string_concatenation_benchmark.py`: `build_join()` (3,048,890 characters in one memory pass).
  - `Q5/canteen_order_scope.py`: `add_item(item, order=None)` resolving mutable default argument bug.
  - `Q6/temple_steps_recursion.py`: `ways_memo()` with `@lru_cache`.
- **Design Challenge (Q7)**: Solves recursive stack exhaustion at $n = 1000$ by redesigning the climbing combinatorics into an $O(1)$ space iterative loop and $O(\log n)$ binary matrix exponentiation algorithm ($n = 50,000$ executes in milliseconds).

### Assignment 3: Python Data Structures (CO3)
- **Key Focus**: Lists and slicing window derivations, hashability and tuple immutability, dictionary frequency analysis, set operations (`&`, `|`, `-`, `^`) for clash detection, generator memory optimization, and nested data indexing.
- **Complete the Code**:
  - `Q2/tuples_and_mutability.py`: List comprehension independent grid generation.
  - `Q3/complaint_analysis.py`: `frequencies()` with `dict.get()` and `top()` tie-breaker sorting.
  - `Q4/elective_clash_detection.py`: Set operators (`&`, `^`, `-`) for course clash detection.
- **Design Challenge (Q7)**: First-principles contact deduplication and entity resolution architecture. Normalizes multi-format phone numbers and emails, grouping records via hash indices in $O(n)$ time while preventing erroneous merging of distinct individuals with identical names.

### Assignment 4: File Handling, Exceptions, Modules and Packages (CO4)
- **Key Focus**: Diagnosing unsafe scripts, streaming I/O with context managers (`with`), custom exception hierarchy (`InvalidRecord`), software forensics on file overwriting and newline omission, and modular packaging.
- **Complete the Code**: `Task03/attendance_exceptions.py`: `parse_line()` and `summarise()`.
- **Design Challenge (Task 06)**: Robust cultural fest registration package (`fest_registration/`) with 3 decoupled modules (`validator`, `processor`, `reporter`). Seamlessly handles missing files, duplicate registrations, and malformed emails with zero unhandled exceptions.

### Assignment 5: Data Analysis, Visualisation and AI Applications (CO5)
- **Key Focus**: Relational SQLite architecture with B-Tree indices, telemetry cleaning and validation, min-max feature scaling, Matplotlib visual analytics, multi-scale performance comparisons (Python Loops vs Pandas vs SQL), and introductory AI (negation-aware sentiment scoring, extractive summarization, and SQL-integrated chatbot).
- **Complete the Code**:
  - `Part-B/B1/cleaning_pipeline.py`: `load_clean()` and `min_max()`.
  - `Part-B/B2/adversarial_testing.py`: `executemany()` and parameterised `station_average()`.
  - `Part-B/B4/final_decision_ai.py`: Negation-aware `score()` algorithm.
- **Deliverables**: SQLite database (`database/air_quality.db`), 4 generated figures (`charts/`), and evaluation across 50 real-world citizen complaints ($\ge 88\%$ human agreement).

---

## 3. Quick Start & Execution Guide

### Step 1: Install Dependencies
Assignments 1 to 4 utilize the Python Standard Library exclusively. Assignment 5 requires `pandas` and `matplotlib`:

```bash
pip install -r Assignment-5/requirements.txt
```

### Step 2: Running Automated Test Suites
Each assignment folder contains a pre-executed `test_results.txt`. You can independently run each suite from the repository root:

```bash
# Assignment 1 Test Suite
python Assignment-1/Task09/test_calculator.py
python Assignment-1/Task12/test_adapted_calculator.py

# Assignment 2 Test Suite
python Assignment-2/Q1/subsidy_eligibility.py
python Assignment-2/Q7/redesign_steps_challenge.py

# Assignment 3 Test Suite
python Assignment-3/Q4/elective_clash_detection.py
python Assignment-3/Q7/contact_merging.py

# Assignment 4 Test Suite
python Assignment-4/Task03/attendance_exceptions.py
python Assignment-4/Task06/run_fest_challenge.py

# Assignment 5 Test Suite
python Assignment-5/Part-B/B1/cleaning_pipeline.py
python Assignment-5/Part-B/B4/final_decision_ai.py
```
