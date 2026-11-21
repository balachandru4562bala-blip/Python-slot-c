"""
TASK 07: Test Script for milkrate Module
Demonstrates:
- import milkrate
- from milkrate import payout
- import milkrate as mr
- Explanation of why the table in milkrate.py is suppressed upon import (__name__ == '__main__')
- Alternative concept analysis: Copying code vs Module import (sys.modules caching)
"""

import sys
import os

# Ensure current folder is in sys.path
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))

# 1. Style 1: standard import
import milkrate

# 2. Style 2: from ... import ...
from milkrate import payout

# 3. Style 3: aliased import
import milkrate as mr

def run_task07_demonstrations():
    print("=" * 60)
    print("TASK 07: MODULE USAGE AND IMPORT DEMONSTRATION")
    print("=" * 60)
    
    print("\n1. Calling via 'milkrate.rate_per_litre':")
    rate = milkrate.rate_per_litre(4.2, 8.7)
    print(f"   Rate for 4.2% fat, 8.7% SNF = Rs {rate:.2f}")
    
    print("\n2. Calling via imported 'payout':")
    pay = payout(8.5, 4.2, 8.7)
    print(f"   Payout for 8.5L = Rs {pay:.2f}")
    
    print("\n3. Calling via alias 'mr.payout':")
    pay_alias = mr.payout(10.0, 3.5, 8.5)
    print(f"   Payout for 10.0L = Rs {pay_alias:.2f}")
    
    print("\n--- Explanation of if __name__ == '__main__': ---")
    print("When milkrate.py was imported above, its test table was NOT printed.")
    print("This is because Python sets __name__ to the string 'milkrate' during import.")
    print("The guard condition `if __name__ == '__main__':` evaluates to False.")
    print("When run directly from the terminal, Python sets __name__ to '__main__', executing the tests.")
    
    print("\n--- sys.modules Caching Demonstration ---")
    print(f"'milkrate' present in sys.modules: {'milkrate' in sys.modules}")
    print("Subsequent imports retrieve the cached module object in O(1) time without re-parsing.")

if __name__ == "__main__":
    run_task07_demonstrations()
