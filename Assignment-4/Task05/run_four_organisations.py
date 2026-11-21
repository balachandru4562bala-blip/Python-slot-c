"""
ASSIGNMENT 4 - TASK 05: The Same Utility Organised Four Ways
Demonstration and Architectural Comparison:
(a) Monolith script
(b) Single library module + main driver
(c) Three decoupled modules (reader, stats, report)
(d) Structured package (attendance_pkg/) with __init__.py

Evaluates:
- Number of files modified for requirement change (3 consecutive absences)
- Readability, reuse, unit-testability, and namespace pollution
- Import semantics explanation
"""

import subprocess
import os
import sys

CURRENT_DIR = os.path.dirname(os.path.abspath(__file__))

def run_task05():
    print("=" * 75)
    print("ASSIGNMENT 4 - TASK 05: CODE ORGANISATION ARCHITECTURAL REVIEW")
    print("=" * 75)

    orgs = [
        ("Organisation A (Monolith)", os.path.join(CURRENT_DIR, "org_a_monolith", "attendance_monolith.py")),
        ("Organisation B (Single Module)", os.path.join(CURRENT_DIR, "org_b_single_module", "main_b.py")),
        ("Organisation C (Three Modules)", os.path.join(CURRENT_DIR, "org_c_three_modules", "main_c.py")),
        ("Organisation D (Package)", os.path.join(CURRENT_DIR, "org_d_package", "main_d.py")),
    ]

    for label, script_path in orgs:
        print(f"\n>>> Running: {label} <<<")
        res = subprocess.run([sys.executable, os.path.basename(script_path)],
                             cwd=os.path.dirname(script_path),
                             capture_output=True, text=True)
        print(res.stdout.strip())

    # Task 5.2: Requirement Change Evaluation
    print("\n--- Task 5.2: Requirement Change Impact Analysis ---")
    print("Requirement: Add a new report identifying students absent for 3 consecutive days.")
    print(f"{'Organisation Structure':<32} | {'Files Changed':<15} | {'Modified Files':<30}")
    print("-" * 80)
    print(f"{'A. Monolith Script':<32} | {'1 file':<15} | {'attendance_monolith.py'}")
    print(f"{'B. Single Module':<32} | {'2 files':<15} | {'attendance_lib.py, main_b.py'}")
    print(f"{'C. Three Decoupled Modules':<32} | {'2 files':<15} | {'stats.py, report.py (reader untouched!)'}")
    print(f"{'D. Structured Package':<32} | {'2 files':<15} | {'stats.py, report.py (clean API barrier)'}")

    # Task 5.3: Comparative Matrix & Import Semantics
    print("\n--- Task 5.3: Architectural Trade-Off Comparison Matrix ---")
    matrix = [
        ("Readability", "High for small scripts, poor at scale", "Moderate", "High (Clean separation)", "Highest (Standardized namespace)"),
        ("Reusability", "Zero (Code copy required)", "High for whole utility", "High (Can reuse only reader.py)", "Maximum (Distributable wheel/egg)"),
        ("Unit Testing", "Difficult (Tightly coupled)", "Moderate", "Easy (Can mock reader for stats)", "Trivial (Isolated submodule tests)"),
        ("Namespace Safety", "Polluted global scope", "Module scope barrier", "Clean decoupled namespaces", "Hierarchical dot-notation isolation"),
    ]
    print(f"{'Criterion':<15} | {'A. Monolith':<22} | {'B. Single Mod':<20} | {'C. 3 Modules':<20} | {'D. Package':<20}")
    print("-" * 105)
    for row in matrix:
        print(f"{row[0]:<15} | {row[1]:<22} | {row[2]:<20} | {row[3]:<20} | {row[4]:<20}")

    print("\n--- Import Semantics Explained ---")
    print("1. `import attendance.stats`:")
    print("   Loads submodule 'stats' inside 'attendance' package into sys.modules.")
    print("   Must be called via full qualified name: `attendance.stats.calculate_stats()`.")
    print("2. `from attendance import stats`:")
    print("   Binds the identifier `stats` into local namespace; called as `stats.calculate_stats()`.")
    print("3. `from attendance.stats import percentage`:")
    print("   Binds ONLY the specific function `percentage` directly into current namespace.")

if __name__ == "__main__":
    run_task05()
