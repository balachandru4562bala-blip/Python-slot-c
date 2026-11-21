"""
ASSIGNMENT 2 - Q4: Building Long Text: + or join()?
Monthly SMS Bill Statement Builder

Includes:
- Complete the Code: TODO 1 build_join(parts)
- Repeated += in loop: build_plus()
- "".join() with parts
- Alternative concepts: io.StringIO and direct file write
- Execution timing at 1,000, 10,000, and 200,000 items
- Detailed explanation of string immutability & CPython realloc optimization
"""

import time
import io
import sys

# Test dataset: 200,000 lines
items = [f"Item{i}:Rs{i % 50}" for i in range(200_000)]

def build_plus(parts):
    text = ""
    for p in parts:
        text += p + ";"
    return text

def build_join(parts):
    # TODO 1: Build the same text using a single str.join() call
    return ";".join(parts) + (";" if parts else "")

def build_stringio(parts):
    """Alternative concept: using io.StringIO mutable character buffer."""
    buf = io.StringIO()
    for p in parts:
        buf.write(p)
        buf.write(";")
    return buf.getvalue()

def run_q4_benchmarks():
    print("=" * 70)
    print("ASSIGNMENT 2 - Q4: STRING CONCATENATION (+ vs JOIN) BENCHMARK")
    print("=" * 70)

    # 1. Assignment exact test run at 200,000 items
    print("\n--- Running 200,000 Items Test (3 Iterations for Average) ---")
    times_plus = []
    times_join = []

    for trial in range(1, 4):
        start = time.perf_counter()
        a = build_plus(items)
        t_plus = time.perf_counter() - start
        times_plus.append(t_plus)

        start = time.perf_counter()
        b = build_join(items)
        t_join = time.perf_counter() - start
        times_join.append(t_join)

        if trial == 1:
            print("same text:", a == b, "| length:", len(b))
        print(f"Trial {trial}: += time: {t_plus:.4f} s | join time: {t_join:.4f} s")

    avg_plus = sum(times_plus) / len(times_plus)
    avg_join = sum(times_join) / len(times_join)
    print(f"\nAverage 200,000 items: += time = {avg_plus:.4f} s | join time = {avg_join:.4f} s")
    print(f"str.join() speedup: {avg_plus / avg_join:.2f}x faster")

    # 2. Scaling benchmark across sizes (1,000, 10,000, 200,000)
    print("\n--- Comparative Multi-Scale Performance Table ---")
    print(f"{'Data Size':<12} | {'+= Time (s)':<15} | {'join() Time (s)':<16} | {'StringIO Time (s)':<18} | {'Speedup':<10}")
    print("-" * 75)

    scales = [1_000, 10_000, 200_000]
    for n in scales:
        subset = items[:n]

        t0 = time.perf_counter()
        r_plus = build_plus(subset)
        t_p = time.perf_counter() - t0

        t0 = time.perf_counter()
        r_join = build_join(subset)
        t_j = time.perf_counter() - t0

        t0 = time.perf_counter()
        r_sio = build_stringio(subset)
        t_s = time.perf_counter() - t0

        assert r_plus == r_join == r_sio
        speedup = f"{t_p / t_j:.2f}x" if t_j > 0 else "N/A"
        print(f"{n:<12} | {t_p:<15.6f} | {t_j:<16.6f} | {t_s:<18.6f} | {speedup:<10}")

    # 3. String Immutability and CPython Optimization Analysis
    print("\n--- Technical Explanation ---")
    print("1. Why += can become O(n^2): Python strings are immutable.")
    print("   In the naive model, `text += p` creates a new buffer and copies all previous characters.")
    print("   Total characters copied = 1 + 2 + ... + n = O(n^2).")
    print("2. CPython Optimization: When reference count of `text` is 1 and no other variable aliases it,")
    print("   CPython's PyUnicode_Append reallocates the buffer in-place using amortized doubling, reducing += to O(n).")
    print("3. Why join() is ALWAYS superior: `str.join()` calculates the exact final buffer length in ONE pass,")
    print("   allocates memory ONCE, and performs memory-copy in C. It is guaranteed O(n) across all Python runtimes.")

if __name__ == "__main__":
    run_q4_benchmarks()
