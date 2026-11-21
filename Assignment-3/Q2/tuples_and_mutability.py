"""
ASSIGNMENT 3 - Q2: Tuples, Mutability and Copying
City Bus-Stop Map & Passenger Zones

Includes:
- Complete the Code: TODO 1 good grid list comprehension
- Aliasing, shallow copy (copy.copy, slicing), deep copy (copy.deepcopy)
- Explaining why tuples are hashable dictionary keys and lists are unhashable
- Memory comparison of 1,000,000 element list vs tuple using sys.getsizeof()
- Timing creation and indexing
- Modifying a mutable list nested inside an immutable tuple
- Alternative concept: Sparse matrix dictionary keyed by (row, col) tuples
"""

import copy
import sys
import time

def run_q2():
    print("=" * 75)
    print("ASSIGNMENT 3 - Q2: TUPLES, MUTABILITY, AND MEMORY ALIASING")
    print("=" * 75)

    # 1. Complete the Code Required Section
    print("\n--- Complete the Code Expected Execution ---")
    rows, cols = 3, 4

    bad = [[0] * cols] * rows # every row is the SAME list object
    bad[0][1] = 7

    # TODO 1: Create a rows x cols grid of zeros using a list comprehension so that every
    # row is a separate list
    good = [[0 for _ in range(cols)] for _ in range(rows)]
    good[0][1] = 7

    print("bad :", bad)
    print("good:", good)
    print(bad[0] is bad[1], good[0] is good[1])

    # Tuples are immutable, so they can be used as dictionary keys
    stops = {(13.0827, 80.2707): "Chennai Central", (13.0418, 80.2341): "T. Nagar"}
    print(stops[(13.0418, 80.2341)])

    # 2. Attempting to use a List as a Dictionary Key
    print("\n--- Unhashable Type Demonstration ---")
    try:
        invalid_dict = {}
        invalid_dict[[13.0418, 80.2341]] = "T. Nagar"
    except TypeError as e:
        print(f"Caught expected TypeError: {e}")
        print("Explanation: Python dictionaries require keys to be hashable (immutable hash value).")
        print("Lists are mutable and do not implement __hash__(); tuples are immutable and hashable.")

    # 3. Tuple Unpacking in For Loops
    print("\n--- Tuple Unpacking in Loops ---")
    bus_routes = [
        ("Stop 1", (13.0827, 80.2707), 45),
        ("Stop 2", (13.0418, 80.2341), 78),
        ("Stop 3", (12.9815, 80.2180), 32),
    ]
    for stop_name, (lat, lon), passengers in bus_routes:
        print(f"Route: {stop_name:<8} | Lat: {lat:<7.4f}, Lon: {lon:<7.4f} | Boarded: {passengers} passengers")

    # 4. Copying Semantics: Aliasing vs Shallow Copy vs Deep Copy
    print("\n--- Copying Semantics Demonstration ---")
    original = [[1, 2], [3, 4]]
    aliased = original
    shallow = copy.copy(original)
    sliced = original[:]
    deep = copy.deepcopy(original)

    # Mutate nested element
    original[0][0] = 999
    print(f"Original after mutating original[0][0]=999 : {original}")
    print(f"Aliased  (same pointer)                   : {aliased} (Mutated!)")
    print(f"Shallow Copy (copy.copy)                  : {shallow} (Nested element mutated!)")
    print(f"Sliced Copy ([:])                         : {sliced} (Nested element mutated!)")
    print(f"Deep Copy (copy.deepcopy)                 : {deep} (Protected! Deeply isolated)")

    # 5. Modifying a List inside a Tuple
    print("\n--- Modifying a Mutable Element Inside a Tuple ---")
    mixed_tuple = ("Chennai", [10, 20, 30])
    print(f"Initial tuple: {mixed_tuple}")
    mixed_tuple[1].append(40)  # Modifying list inside tuple
    print(f"After mixed_tuple[1].append(40): {mixed_tuple}")
    print("Explanation: The tuple contains object references. The reference to the list is fixed (immutable),")
    print("but the list object itself is mutable in-place.")

    # 6. Memory and Speed Comparison: 1,000,000 Elements
    print("\n--- Memory and Indexing: List vs Tuple (1,000,000 items) ---")
    n_items = 1_000_000

    # Creation timing
    t0 = time.perf_counter()
    sample_list = list(range(n_items))
    t_create_list = time.perf_counter() - t0

    t0 = time.perf_counter()
    sample_tuple = tuple(range(n_items))
    t_create_tuple = time.perf_counter() - t0

    mem_list = sys.getsizeof(sample_list)
    mem_tuple = sys.getsizeof(sample_tuple)

    print(f"Memory for list ({n_items} items) : {mem_list} bytes ({mem_list / (1024*1024):.2f} MB)")
    print(f"Memory for tuple ({n_items} items): {mem_tuple} bytes ({mem_tuple / (1024*1024):.2f} MB)")
    print(f"Memory saved by tuple: {mem_list - mem_tuple} bytes (approx {((mem_list - mem_tuple)/mem_list)*100:.1f}% savings)")

    # Indexing timing
    iters = 1_000_000
    t0 = time.perf_counter()
    for _ in range(iters):
        _ = sample_list[500_000]
    t_idx_list = time.perf_counter() - t0

    t0 = time.perf_counter()
    for _ in range(iters):
        _ = sample_tuple[500_000]
    t_idx_tuple = time.perf_counter() - t0

    print(f"Time for {iters} index operations (List) : {t_idx_list:.4f} s")
    print(f"Time for {iters} index operations (Tuple): {t_idx_tuple:.4f} s")

    # 7. Alternative Concept: Sparse Matrix Dictionary
    print("\n--- Alternative Concept: Sparse Grid Dictionary ---")
    # For a 1000 x 1000 grid with only 5 non-empty passenger zones:
    sparse_grid = {
        (12, 45): 7,
        (100, 250): 15,
        (450, 800): 23,
    }
    print(f"Passenger count at zone (12, 45): {sparse_grid.get((12, 45), 0)}")
    print(f"Passenger count at empty zone (0, 0): {sparse_grid.get((0, 0), 0)}")
    print(f"Memory for sparse dict: {sys.getsizeof(sparse_grid)} bytes vs {sys.getsizeof([[0]*1000 for _ in range(1000)])} bytes for 1000x1000 matrix!")

if __name__ == "__main__":
    run_q2()
