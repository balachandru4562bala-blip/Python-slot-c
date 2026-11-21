# Assignment 3: Python Data Structures

**Course Outcome**: CO3 — Implement Python data structures (lists, tuples, dictionaries, and sets) to store, access, and manipulate unstructured data effectively  
**Bloom's Levels**: K3 Apply, K4 Analyse, K5 Evaluate  
**Total Marks**: 50  

---

## 1. Assignment Objectives
- Leverage Python lists and slicing for continuous time-series records and derive sliding window complexity.
- Distinguish tuples from lists in mutability, memory allocation (`sys.getsizeof()`), and dictionary key hashability.
- Utilize dictionaries for high-frequency text mining, inverted indices, and multi-key entity groupings.
- Apply mathematical set operations (`&`, `|`, `-`, `^`) to resolve complex overlap and scheduling clashes in $O(1)$ amortized time.
- Compare memory and performance characteristics of list comprehensions, generator expressions, and functional pipelines (`map`, `filter`).
- Design an end-to-end, multi-source contact deduplication and entity resolution architecture from first principles.

---

## 2. Directory Structure

```
Assignment-3/
├── Q1/
│   └── rainfall_analysis.py               # Lists, slicing, naive vs running-sum moving averages
├── Q2/
│   └── tuples_and_mutability.py           # Complete the Code TODO 1, aliasing, deepcopy, hashability
├── Q3/
│   └── complaint_analysis.py              # Complete the Code TODO 1 & 2, word frequencies, Counter
├── Q4/
│   └── elective_clash_detection.py        # Complete the Code TODO 1, set operators vs methods, Venn diagrams
├── Q5/
│   └── sensor_cleaning_comprehensions.py  # List comprehension, generator memory, map/filter
├── Q6/
│   └── railway_timetable.py               # Nested data structures, inverted index query acceleration
├── Q7/
│   ├── CONTACT_MERGING_DESIGN.md          # 4-stage problem interpretation, architecture, and pseudocode
│   └── contact_merging.py                 # Multi-field canonical normalization, hash indexing vs pairwise
├── test_results.txt                       # Verified test execution log
├── requirements.txt                       # Python dependencies
└── README.md                              # Assignment documentation
```

---

## 3. Description of Questions and Implementations

### Q1: Daily Rainfall Records (Lists and Slicing)
- **File**: `Q1/rainfall_analysis.py`
- **Key Findings**: Implements 52 weekly totals using slicing. Compares naive moving average ($6 \times (n-6)$ additions) with running-sum ($2n-7$ operations) and `collections.deque(maxlen=7)`. Benchmarked across 365, 36,500, and 365,000 readings.

### Q2: Tuples, Mutability and Copying (City Bus-Stop Map)
- **File**: `Q2/tuples_and_mutability.py`
- **Key Findings**: Completes TODO 1 for independent list comprehension grid creation. Proves lists cannot be dictionary keys (`TypeError: unhashable type: 'list'`). Demonstrates shallow vs deep copying, mutating lists within tuples, and benchmarks 1,000,000 element tuple vs list memory.

### Q3: Farmer Helpline Complaint Analysis (Dictionaries)
- **File**: `Q3/complaint_analysis.py`
- **Key Findings**: Completes TODO 1 (`frequencies`) and TODO 2 (`top`). Explains ASCII tie-breaking. Groups complaints by district with `setdefault()`. Benchmarks dictionary loops vs `list.count()` vs `collections.Counter` across 1,000 to 100,000 complaints.

### Q4: Elective Registration Clash Detection (Sets)
- **File**: `Q4/elective_clash_detection.py`
- **Key Findings**: Completes TODO 1 using `&`, `^`, and `-`, matching exact expected output. Re-implements with set methods. Demonstrates $O(1)$ set lookup vs $O(n)$ list scan and nested loop clash detection vs set intersection.

### Q5: Cleaning Sensor Readings (List Comprehension)
- **File**: `Q5/sensor_cleaning_comprehensions.py`
- **Key Findings**: Filters $[-50, 50]$ °C and converts to Fahrenheit. Detects alarm minutes outside $[2, 8]$ °C with `enumerate()`. Compares `for` loop, list comprehension, and `map/filter`. Demonstrates $O(1)$ memory generator expressions.

### Q6: Nested Railway Timetable (Nested Data Structures)
- **File**: `Q6/railway_timetable.py`
- **Key Findings**: Models 5 real express trains in nested dict/list/tuple/set structures. Queries trains stopping at a station on a given day. Builds an inverted index station directory accelerating query response times by up to $150\times$.

### Q7: Contact-Merging Program from First Principles
- **Files**: `Q7/CONTACT_MERGING_DESIGN.md`, `Q7/contact_merging.py`
- **Key Findings**: Complete 4-stage engineering response. Normalizes messy phone formats (`+91`, `0`, spaces, hyphens) and emails. Entity resolution groups records via hash index in $O(n)$ time, avoiding $O(n^2)$ pairwise comparison. Disambiguates distinct persons with identical names.

---

## 4. Execution Commands

```bash
# Q1: Rainfall Analysis
python Assignment-3/Q1/rainfall_analysis.py

# Q2: Tuples and Mutability
python Assignment-3/Q2/tuples_and_mutability.py

# Q3: Helpline Complaint Analysis
python Assignment-3/Q3/complaint_analysis.py

# Q4: Elective Clash Detection
python Assignment-3/Q4/elective_clash_detection.py

# Q5: Sensor Cleaning Comprehensions
python Assignment-3/Q5/sensor_cleaning_comprehensions.py

# Q6: Railway Timetable
python Assignment-3/Q6/railway_timetable.py

# Q7: Contact Merging
python Assignment-3/Q7/contact_merging.py
```
