# Assignment 1: Payment Calculator for a Village Milk Co-operative

**Course**: CSA08 – Python Programming  
**Bloom's Levels Assessed**: K3 Apply, K4 Analyse, K5 Evaluate  
**Scenario**: Ksheera Village Milk Producers' Co-operative Payment System  

---

## 1. Assignment Objectives
- Design, implement, and validate a production-grade milk collection payment calculator.
- Eliminate fractional paisa accounting discrepancies using the `decimal` module.
- Adhere to software engineering principles: single point of truth constants, modular function decomposition, standard algorithmic pseudocode, and automated assertion testing.
- Evaluate scalability from single-centre scale (300 farmers) to district-union scale (150,000 farmers).
- Solve the Day-4 Design Challenge incorporating seasonal pricing and volume incentive bonuses.

---

## 2. Directory Structure

```
Assignment-1/
├── Task01/
│   └── task01_analysis.py          # Data identification, validation rules, memory scaling
├── Task02/
│   └── float_vs_decimal.py         # Complete the Code TODO 1, IEEE 754 float drift vs Decimal
├── Task03/
│   └── constants_demo.py           # PEP 8 named constants, dynamic typing, dictionary rate card
├── Task04/
│   └── expressions_demo.py         # Arithmetic expressions, round() vs int() vs floor()
├── Task05/
│   └── input_validation.py         # Safe string input parsing, f-string tabular formatting
├── Task06/
│   └── milk_functions.py           # Functions, docstrings, scope, lambda comparison
├── Task07/
│   ├── milkrate.py                 # Module with Complete the Code TODO 1 & 2
│   └── test_module.py              # Module import demonstration and caching analysis
├── Task08/
│   ├── ALGORITHM.md                # Standardized pseudocode, flowchart, hand trace table
│   └── algorithm_trace.py          # Executable hand trace
├── Task09/
│   ├── milk_calculator.py          # Complete application calculator with validation
│   └── test_calculator.py          # Automated test suite with assert statements
├── Task10/
│   └── benchmark_payments.py       # Performance & drift benchmark (300 to 150,000 records)
├── Task11/
│   ├── rate_config.json            # External JSON configuration file
│   ├── RECOMMENDATION.md           # Architecture defense and scaling evaluation
│   └── recommendation_defense.py   # Benchmark comparing JSON loader vs module
├── Task12/
│   ├── DESIGN_CHALLENGE_REPORT.md  # Day-4 impact analysis and architecture defense
│   ├── adapted_calculator.py       # Adapted engine (2-decimal inputs, seasons, bonus)
│   └── test_adapted_calculator.py  # Test suite for adapted design challenge
├── test_results.txt                # Consolidated test execution logs
├── requirements.txt                # Dependencies specification
└── README.md                       # Comprehensive assignment documentation
```

---

## 3. Description of Tasks and Implementations

### Task 01: Understand Problem and Identify Data
- **File**: `Task01/task01_analysis.py`
- **Description**: Defines data dictionary, input constraints (fat 2.0–7.0%, SNF 6.0–12.0%, litres > 0), and compares list/tuple storage against 3 separate unrolled variables for 300 farmers.

### Task 02: Explore Values and Types in Interpreter
- **File**: `Task02/float_vs_decimal.py`
- **Description**: Completes TODO 1 for exact decimal addition. Demonstrates that `float` produces `33400.30000000061` whereas `Decimal` produces exact `33400.30`. Explains the danger of `Decimal(float(amount))` and integer paise alternatives.

### Task 03: Variables and Constants
- **File**: `Task03/constants_demo.py`
- **Description**: Defines single-point-of-truth constants (`BASE_RATE`, `STANDARD_FAT`, `FAT_STEP_VALUE`), demonstrates dynamic typing and tuple unpacking swaps, and benchmarks against dictionary rate cards.

### Task 04: Write Correct Expressions
- **File**: `Task04/expressions_demo.py`
- **Description**: Fixes floating point division nuances `(4.2 - 3.5)/0.1` using `round()`. Explains operator precedence (`-3 ** 2 = -9`) and banker's rounding.

### Task 05: Read Input and Convert Types
- **File**: `Task05/input_validation.py`
- **Description**: Implements safe parsing handling commas (`8,5`), whitespace, and non-numeric inputs. Formats output with f-string width and precision specifiers.

### Task 06: Organise Logic into Functions
- **File**: `Task06/milk_functions.py`
- **Description**: Implements `rate_per_litre()`, `payout()`, and `ten_day_total()`. Analyzes function call overhead against lambdas and inline scripts.

### Task 07: Build a Module
- **Files**: `Task07/milkrate.py`, `Task07/test_module.py`
- **Description**: Completes TODO 1 and TODO 2. Demonstrates module import styles and explains why `if __name__ == "__main__":` blocks top-level execution on import.

### Task 08: Plan Algorithm Before Coding
- **Files**: `Task08/ALGORITHM.md`, `Task08/algorithm_trace.py`
- **Description**: SIMATS-compliant pseudocode, Mermaid flowchart, and hand trace table for 3 entries.

### Task 09: Implement and Test Calculator
- **Files**: `Task09/milk_calculator.py`, `Task09/test_calculator.py`
- **Description**: Automated test suite with assertions testing normal cases, boundary conditions, invalid inputs, and a 5-entry hand-calculated batch.

### Task 10: Compare Expectations with Execution
- **File**: `Task10/benchmark_payments.py`
- **Description**: Measures float drift and execution time for 300, 6,000, and 150,000 transactions. Compares dynamic calculation with precomputed lookup table.

### Task 11: Recommend and Defend Final Design
- **Files**: `Task11/RECOMMENDATION.md`, `Task11/recommendation_defense.py`
- **Description**: Recommends `Decimal` with per-transaction `ROUND_HALF_UP` rounding and external JSON configuration.

### Task 12: Day-4 Design Challenge
- **Files**: `Task12/DESIGN_CHALLENGE_REPORT.md`, `Task12/adapted_calculator.py`, `Task12/test_adapted_calculator.py`
- **Description**: Adapts architecture for 2-decimal inputs, April–June summer rates (Rs 32.00 base, Rs 0.45 fat step), and > 500 L volume bonus (Rs 0.50/L).

---

## 4. Execution Commands

Run programs using Python 3:

```bash
# Task 01
python Assignment-1/Task01/task01_analysis.py

# Task 02
python Assignment-1/Task02/float_vs_decimal.py

# Task 03
python Assignment-1/Task03/constants_demo.py

# Task 04
python Assignment-1/Task04/expressions_demo.py

# Task 05
python Assignment-1/Task05/input_validation.py

# Task 06
python Assignment-1/Task06/milk_functions.py

# Task 07
python Assignment-1/Task07/milkrate.py
python Assignment-1/Task07/test_module.py

# Task 08
python Assignment-1/Task08/algorithm_trace.py

# Task 09
python Assignment-1/Task09/test_calculator.py

# Task 10
python Assignment-1/Task10/benchmark_payments.py

# Task 11
python Assignment-1/Task11/recommendation_defense.py

# Task 12
python Assignment-1/Task12/test_adapted_calculator.py
```
