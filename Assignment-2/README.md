# Assignment 2: Python Control Flow and String Operations

**Course Outcome**: CO2 — Analyse control flow constructs, string operations, and functions  
**Bloom's Levels**: K3 Apply, K4 Analyse, K5 Evaluate  
**Total Marks**: 50  

---

## 1. Assignment Objectives
- Master branch evaluation and boundary conditions with `if`, `if-else`, and `if-elif-else`.
- Implement robust iteration mechanisms using `while`, `for`, `break`, `continue`, `pass`, and loop `else`.
- Engineer string processing tools without regex using indexing, slicing, and string methods.
- Analyze algorithmic efficiency and memory characteristics of string building (`+=` vs `join()` vs `StringIO`).
- Investigate function parameter passing, default argument lifecycles, and Python scope resolution (`LEGB`).
- Explore recursion mechanics, call stack exhaustion (`RecursionError`), and dynamic programming optimizations.
- Execute the Day-4 Design Challenge by diagnosing, redesigning, and validating an optimal combinatorial algorithm.

---

## 2. Directory Structure

```
Assignment-2/
├── Q1/
│   └── subsidy_eligibility.py             # Electricity subsidy eligibility boundary analysis
├── Q2/
│   └── otp_verification.py               # OTP verification loop, break/continue/else, security retry
├── Q3/
│   └── vehicle_validator.py              # Complete the Code TODO 1 & 2, slicing vs regex
├── Q4/
│   └── string_concatenation_benchmark.py # Complete the Code TODO 1, += vs join() benchmark
├── Q5/
│   └── canteen_order_scope.py            # Complete the Code TODO 1, default parameter bug & scopes
├── Q6/
│   └── temple_steps_recursion.py         # Complete the Code TODO 1, naive vs memoised call tree
├── Q7/
│   ├── DESIGN_CHALLENGE_Q7.md            # Diagnosis, objective, algorithm design, and defense
│   └── redesign_steps_challenge.py       # Iterative O(1) space & Matrix Exponentiation O(log n)
├── test_results.txt                      # Verified test execution log
├── requirements.txt                      # Python dependencies
└── README.md                             # Assignment documentation
```

---

## 3. Description of Questions and Implementations

### Q1: Decisions with Many Boundaries (State Electricity Subsidy)
- **File**: `Q1/subsidy_eligibility.py`
- **Key Findings**: Demonstrates that independent `if` statements cause households on boundary edges to be awarded duplicate subsidies. The chained `if-elif-else` construct ensures mutual exclusivity. Tested across 8 boundary households (0, 100, 101, 150, 200, 201 units).

### Q2: Loops that Count Attempts (Bank Kiosk OTP Verification)
- **File**: `Q2/otp_verification.py`
- **Key Findings**: Demonstrates `while` and `for` loops. Empty inputs trigger `continue` without incrementing attempt counters. Loop `else` triggers an account lockout only when all attempts are exhausted without a `break`.

### Q3: Vehicle Registration Number Validator
- **File**: `Q3/vehicle_validator.py`
- **Key Findings**: Completes TODO 1 (`normalise`) and TODO 2 (`is_valid`) using only string slicing and methods. Explains string immutability, `upper()`, and negative indexing (`s[-4:]`).

### Q4: Building Long Text: + or join()?
- **File**: `Q4/string_concatenation_benchmark.py`
- **Key Findings**: Completes TODO 1 for `build_join`. Demonstrates that `join()` achieves 3,048,890 characters in a single memory allocation. Evaluates 1,000, 10,000, and 200,000 lines across 3 trials.

### Q5: Functions, Parameters and Scope (College Canteen Order System)
- **File**: `Q5/canteen_order_scope.py`
- **Key Findings**: Completes TODO 1 resolving the mutable default argument bug (`order=None`). Inspects `__defaults__` to prove list persistence across calls. Demonstrates `local`, `global`, and `nonlocal` scoping.

### Q6: Recursion and Its Limits (Counting Temple Steps)
- **File**: `Q6/temple_steps_recursion.py`
- **Key Findings**: Completes TODO 1 with `@lru_cache`. Hand traces $n = 1$ to 6 ($1, 2, 3, 5, 8, 13$). Demonstrates call tree for $n=5$, call counts for $n = 10, 20, 25, 30$, and handles `RecursionError` at $n = 1000$.

### Q7: Day-4 Design Challenge: Diagnose, Redesign and Validate
- **Files**: `Q7/DESIGN_CHALLENGE_Q7.md`, `Q7/redesign_steps_challenge.py`
- **Key Findings**: Diagnoses recursive call stack exhaustion. Replaces with an $O(1)$ auxiliary space iterative loop and an $O(\log n)$ matrix exponentiation algorithm, successfully computing $n = 50,000$ steps in milliseconds with zero recursion errors.

---

## 4. Execution Commands

```bash
# Q1: Electricity Subsidy
python Assignment-2/Q1/subsidy_eligibility.py

# Q2: OTP Verification
python Assignment-2/Q2/otp_verification.py

# Q3: Vehicle Registration Validator
python Assignment-2/Q3/vehicle_validator.py

# Q4: String Concatenation Benchmark
python Assignment-2/Q4/string_concatenation_benchmark.py

# Q5: Canteen Order & Scope
python Assignment-2/Q5/canteen_order_scope.py

# Q6: Temple Steps Recursion
python Assignment-2/Q6/temple_steps_recursion.py

# Q7: Day-4 Design Challenge
python Assignment-2/Q7/redesign_steps_challenge.py
```
