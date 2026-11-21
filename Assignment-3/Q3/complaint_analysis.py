"""
ASSIGNMENT 3 - Q3: Dictionaries: Farmer Helpline Complaint Analysis
Kisan Call Centre

Includes:
- Complete the Code: TODO 1 frequencies(texts, stop), TODO 2 top(counts, k)
- Grouping complaints by district using dict.setdefault()
- Explanation of hash table lookup O(1) and Python 3.7+ insertion ordering
- Benchmark for 1,000, 10,000, and 100,000 complaints: Dict loop vs list.count() vs Counter
- Engineering decision for 100,000 complaints/day
"""

import collections
import random
import time
import sys

# 1. Complete the Code Section
calls = [
    "seeds not received seeds delayed",
    "fertiliser price high",
    "seeds price high subsidy not received",
]
STOP = {"not", "high"}

def frequencies(texts, stop):
    # TODO 1: Return a dictionary word -> count for every word that is not in stop,
    # using dict.get()
    counts = {}
    for text in texts:
        for word in text.split():
            if word not in stop:
                counts[word] = counts.get(word, 0) + 1
    return counts

def top(counts, k):
    # TODO 2: Return the k most frequent (word, count) pairs, highest count first and
    # alphabetical for ties
    return sorted(counts.items(), key=lambda item: (-item[1], item[0]))[:k]

def group_by_district(complaints_data):
    """
    Groups complaint strings by district name using setdefault().
    complaints_data: list of (district, complaint_text)
    """
    grouped = {}
    for district, text in complaints_data:
        grouped.setdefault(district, []).append(text)
    return grouped

# Alternative Concept 1: Using list.count() on distinct words (O(n * d))
def count_with_list_count(tokens):
    distinct_words = list(set(tokens))
    return {w: tokens.count(w) for w in distinct_words}

# Alternative Concept 2: Using collections.Counter
def count_with_counter(tokens):
    return collections.Counter(tokens)

def run_q3():
    print("=" * 75)
    print("ASSIGNMENT 3 - Q3: DICTIONARIES & HELPLINE COMPLAINT ANALYSIS")
    print("=" * 75)

    # 1. Assignment Required Execution
    print("\n--- Complete the Code Expected Execution ---")
    freqs = frequencies(calls, STOP)
    top_3 = top(freqs, 3)
    print(top_3)

    print("\n--- Explanation of Output Ordering ---")
    print("Expected: [('seeds', 3), ('price', 2), ('received', 2)]")
    print("Why 'price' precedes 'received': Both have count = 2, so the tie-breaker is item[0] (word string).")
    print("Since 'p' < 'r' in ASCII alphabetical order, 'price' is ranked ahead of 'received'.")

    # 2. Grouping by District with setdefault()
    district_records = [
        ("Madurai", "Delay in urea subsidy release"),
        ("Thanjavur", "Paddy seeds quality substandard"),
        ("Madurai", "Porewell electricity connection pending"),
        ("Coimbatore", "Drip irrigation pipe damaged"),
        ("Thanjavur", "Water release schedule delayed"),
    ]
    grouped = group_by_district(district_records)
    print("\n--- Complaints Grouped by District (setdefault) ---")
    for dist, complaints in grouped.items():
        print(f"District: {dist:<12} | Total: {len(complaints)} complaints -> {complaints}")

    # 3. Dictionary Views Demonstration
    print("\n--- Dictionary Views (keys, values, items) ---")
    sample_d = {"paddy": 120, "wheat": 85, "cotton": 45}
    print(f"dict.keys()   (dynamic set-like view)  : {sample_d.keys()}")
    print(f"dict.values() (dynamic collection view): {sample_d.values()}")
    print(f"dict.items()  (dynamic pair view)      : {sample_d.items()}")

    # 4. Experimental Investigation & Benchmarking
    print("\n--- Performance Comparison across Scales ---")
    print(f"{'Complaints':<12} | {'Dict Loop (s)':<16} | {'Counter (s)':<15} | {'list.count() (s)':<18}")
    print("-" * 65)

    vocab = ["seeds", "fertiliser", "water", "electricity", "subsidy", "loan", "crop", "damage", "pesticide", "delayed"]
    scales = [1_000, 10_000, 100_000]

    for n in scales:
        dataset = [" ".join(random.choices(vocab, k=8)) for _ in range(n)]
        all_tokens = [w for text in dataset for w in text.split()]

        # Dict loop
        t0 = time.perf_counter()
        frequencies(dataset, STOP)
        t_dict = time.perf_counter() - t0

        # Counter
        t0 = time.perf_counter()
        _ = count_with_counter(all_tokens)
        t_counter = time.perf_counter() - t0

        # list.count() - only run up to 10k to prevent hanging
        if n <= 10_000:
            t0 = time.perf_counter()
            _ = count_with_list_count(all_tokens)
            t_list_count = f"{time.perf_counter() - t0:.4f}"
        else:
            t_list_count = "Omitted (O(n*d) too slow)"

        print(f"{n:<12} | {t_dict:<16.4f} | {t_counter:<15.4f} | {t_list_count:<18}")

    print("\n--- Engineering Decision for 100,000 Complaints/Day ---")
    print("Recommendation: Deploy collections.Counter or native dict.get() loop.")
    print("Justification : Dict and Counter run in linear O(n) time using C-level hash lookups.")
    print("list.count() executes an O(n) scan for each distinct word (total O(n * d)), causing severe latency.")

if __name__ == "__main__":
    run_q3()
