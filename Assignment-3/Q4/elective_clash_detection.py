"""
ASSIGNMENT 3 - Q4: Sets: Elective Registration Clash Detection
Academic Office Course Registration System

Includes:
- Complete the Code: TODO 1 using set operators (&, ^, -, |)
- Method equivalents: intersection, symmetric_difference, difference, union
- Venn diagram representation
- Hash table mechanics: why x in set is O(1) vs x in list O(n)
- Why sets can contain tuples but not lists (hashability)
- Benchmarks for 10,000, 100,000, 1,000,000 elements: in list vs in set
- Clash detection comparison: Nested loops O(n*m) vs Set Intersection O(n+m)
"""

import time
import random
import sys

def run_q4():
    print("=" * 75)
    print("ASSIGNMENT 3 - Q4: SETS & ELECTIVE CLASH DETECTION")
    print("=" * 75)

    # 1. Complete the Code Required Section
    print("\n--- Complete the Code Expected Execution (Operators) ---")
    ai_elective = {"192311001", "192311004", "192311007", "192311009"}
    iot_elective = {"192311002", "192311004", "192311009", "192311010"}
    all_students = {f"1923110{i:02d}" for i in range(1, 11)}

    # TODO 1: Use set operators to find: students in both electives, students in exactly
    # one, and students in neither
    both = ai_elective & iot_elective
    exactly_one = ai_elective ^ iot_elective
    neither = all_students - (ai_elective | iot_elective)

    print("clash :", sorted(both))
    print("exactly one:", sorted(exactly_one))
    print("neither :", sorted(neither))

    assert sorted(both) == ['192311004', '192311009']
    assert sorted(exactly_one) == ['192311001', '192311002', '192311007', '192311010']
    assert sorted(neither) == ['192311003', '192311005', '192311006', '192311008']

    # 2. Rewriting with Set Methods
    print("\n--- Equivalent Set Methods Execution ---")
    both_meth = ai_elective.intersection(iot_elective)
    exactly_one_meth = ai_elective.symmetric_difference(iot_elective)
    neither_meth = all_students.difference(ai_elective.union(iot_elective))

    print("clash (method)       :", sorted(both_meth))
    print("exactly one (method) :", sorted(exactly_one_meth))
    print("neither (method)     :", sorted(neither_meth))

    assert both == both_meth and exactly_one == exactly_one_meth and neither == neither_meth
    print("[PASS] Method calls produce identical results to operator syntax.")

    # 3. Venn Diagram Visualization
    print("\n--- Venn Diagram Representation ---")
    venn = """
    +-----------------------------------------------------------+
    | All Students (192311001 to 192311010)                     |
    |                                                           |
    |    +--------------------+       +--------------------+    |
    |    | AI Elective Only   | Clash | IoT Elective Only  |    |
    |    | 192311001          | 004   | 192311002          |    |
    |    | 192311007          | 009   | 192311010          |    |
    |    +--------------------+       +--------------------+    |
    |                                                           |
    |    Neither Registered: 003, 005, 006, 008                 |
    +-----------------------------------------------------------+
    """
    print(venn)

    # 4. Hashability: Why Sets Accept Tuples but Reject Lists
    print("--- Hashability & Immutability Demonstration ---")
    try:
        invalid_set = {["192311001", "AI"]}
    except TypeError as e:
        print(f"Caught expected TypeError adding list to set: {e}")
    valid_set_with_tuple = {("192311001", "AI"), ("192311002", "IoT")}
    print(f"Valid set containing tuples: {valid_set_with_tuple}")

    # 5. Experimental Benchmarks: Membership Testing (x in list vs x in set)
    print("\n--- Membership Testing Benchmark: x in list vs x in set ---")
    print(f"{'Data Size':<12} | {'List Lookup Time (s)':<22} | {'Set Lookup Time (s)':<22} | {'Speedup':<10}")
    print("-" * 70)

    scales = [10_000, 100_000, 1_000_000]
    for n in scales:
        sample_list = list(range(n))
        sample_set = set(sample_list)
        target = n - 1  # Worst-case search target at tail

        iters = 500
        # List search
        t0 = time.perf_counter()
        for _ in range(iters):
            _ = target in sample_list
        t_list = time.perf_counter() - t0

        # Set search
        t0 = time.perf_counter()
        for _ in range(iters):
            _ = target in sample_set
        t_set = time.perf_counter() - t0

        speedup = f"{t_list / t_set:.1f}x" if t_set > 0 else "N/A"
        print(f"{n:<12} | {t_list:<22.6f} | {t_set:<22.6f} | {speedup:<10}")

    # 6. Clash Detection Comparison: Nested Loops vs Set Intersection (&)
    print("\n--- Clash Detection: Nested Loops O(n*m) vs Set Intersection O(n+m) ---")
    list_a = list(range(0, 5000))
    list_b = list(range(2500, 7500))
    set_a = set(list_a)
    set_b = set(list_b)

    t0 = time.perf_counter()
    clashes_loop = [x for x in list_a if x in list_b]
    t_loop = time.perf_counter() - t0

    t0 = time.perf_counter()
    clashes_set = set_a & set_b
    t_set_op = time.perf_counter() - t0

    print(f"Nested loop search time (5,000 items) : {t_loop:.4f} s")
    print(f"Set intersection time (&)             : {t_set_op:.6f} s")
    print(f"Speedup from Set Intersection: {t_loop / t_set_op:.1f}x")

if __name__ == "__main__":
    run_q4()
