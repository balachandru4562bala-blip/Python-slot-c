"""
ASSIGNMENT 2 - Q6: Recursion and Its Limits
Counting Ways to Climb Temple Steps (1 or 2 steps at a time)

Includes:
- Complete the Code: TODO 1 in ways_memo(n)
- Hand trace verification for n = 1 to 6
- Growth investigation: call counts for n = 10, 20, 25, 30
- sys.getrecursionlimit() analysis and ways_memo(1000) RecursionError handling
- Alternative concept: O(n) time, O(1) space iterative loop
- Call tree diagram for n = 5
"""

from functools import lru_cache
import sys
import time

calls = 0

def ways_naive(n):
    """Ways to climb n temple steps taking 1 or 2 steps at a time."""
    global calls
    calls += 1
    if n <= 1:
        return 1
    return ways_naive(n - 1) + ways_naive(n - 2)

@lru_cache(maxsize=None)
def ways_memo(n):
    global calls
    calls += 1
    # TODO 1: Write the same base case and recursive case as ways_naive, calling
    # ways_memo
    if n <= 1:
        return 1
    return ways_memo(n - 1) + ways_memo(n - 2)

def ways_iterative(n):
    """Alternative concept: Iterative loop keeping only last two values."""
    if n <= 1:
        return 1
    prev2, prev1 = 1, 1
    for _ in range(2, n + 1):
        curr = prev1 + prev2
        prev2, prev1 = prev1, curr
    return prev1

def print_call_tree_n5():
    """Visualizes the overlapping redundant subproblems for n=5."""
    tree = """
    Call Tree for ways(5):
                     w(5)
              /               \\
            w(4)              w(3)
           /    \\            /    \\
        w(3)    w(2)       w(2)   w(1)
       /   \\    /   \\     /   \\
     w(2) w(1) w(1) w(0) w(1) w(0)
    /   \\
  w(1) w(0)
    Notice: w(3) is evaluated 2 times; w(2) is evaluated 3 times; w(1) is evaluated 5 times!
    """
    print(tree)

def run_q6():
    global calls
    print("=" * 70)
    print("ASSIGNMENT 2 - Q6: RECURSION, MEMOISATION & CALL STACK LIMITS")
    print("=" * 70)

    # 1. Complete the Code Required Execution
    print("\n--- Complete the Code Expected Execution ---")
    calls = 0
    res_naive = ways_naive(25)
    calls_naive = calls
    print(f"naive: {res_naive} calls = {calls_naive}")

    calls = 0
    ways_memo.cache_clear()
    res_memo = ways_memo(25)
    calls_memo = calls
    print(f"memo : {res_memo} calls = {calls_memo}")

    assert res_naive == 121393 and calls_naive == 242785
    assert res_memo == 121393 and calls_memo == 26

    # 2. Hand-Calculated Verification (n = 1 to 6)
    print("\n--- Hand Trace Verification for n = 1 to 6 ---")
    expected_hand = {1: 1, 2: 2, 3: 3, 4: 5, 5: 8, 6: 13}
    for k, exp in expected_hand.items():
        actual = ways_iterative(k)
        print(f"n = {k}: expected = {exp}, actual = {actual} -> {'PASS' if exp == actual else 'FAIL'}")
        assert actual == exp

    print("\n--- Call Tree Diagram for n = 5 ---")
    print_call_tree_n5()

    # 3. Growth Investigation: Naive vs Memoised
    print("\n--- Growth Investigation: Function Call Counts ---")
    print(f"{'n':<6} | {'Answer':<12} | {'Naive Calls':<15} | {'Memo Calls':<12} | {'Calls Ratio (Naive/Memo)':<25}")
    print("-" * 75)

    test_ns = [10, 20, 25, 30]
    for val in test_ns:
        # Memoised
        ways_memo.cache_clear()
        calls = 0
        ans = ways_memo(val)
        c_memo = calls

        # Naive
        calls = 0
        ways_naive(val)
        c_naive = calls

        ratio = f"{c_naive / c_memo:.1f}x"
        print(f"{val:<6} | {ans:<12} | {c_naive:<15} | {c_memo:<12} | {ratio:<25}")

    # 4. Deployment Decision: sys.getrecursionlimit() and n = 1000
    print("\n--- Deployment Decision & Recursion Limit Investigation ---")
    rec_limit = sys.getrecursionlimit()
    print(f"Current sys.getrecursionlimit() = {rec_limit}")

    # Test ways_memo(1000)
    ways_memo.cache_clear()
    try:
        ways_memo(1000)
        print("ways_memo(1000) succeeded.")
    except RecursionError as e:
        print(f"Caught expected RecursionError on ways_memo(1000): {e}")
        print("Reason: 1,000 recursive frames exceeded default Python stack limit.")

    # Iterative version at n = 1,000
    t0 = time.perf_counter()
    ans_1000 = ways_iterative(1000)
    t_iter_1000 = time.perf_counter() - t0
    digits_count = len(str(ans_1000))
    print(f"\nIterative ways_iterative(1000) succeeded in {t_iter_1000 * 1000:.3f} ms!")
    print(f"Result has {digits_count} digits (First 20 digits: {str(ans_1000)[:20]}...)")

    print("\n--- Summary Complexity Comparison ---")
    print("1. Plain Recursion  : Time O(phi^n) ~ O(1.618^n) [Exponential], Space O(n) Call Stack")
    print("2. Memoised (Cache) : Time O(n) [Linear], Space O(n) Call Stack + O(n) Cache")
    print("3. Iterative Loop   : Time O(n) [Linear], Space O(1) [Auxiliary Constant Space] -> BEST FOR PRODUCTION")

if __name__ == "__main__":
    run_q6()
