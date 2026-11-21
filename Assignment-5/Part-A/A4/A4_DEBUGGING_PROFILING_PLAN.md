# TASK A4: PLAN DEBUGGING AND PROFILING

---

### A4.1: Comprehensive Debugging Plan

1. **Print Statements**: Used strictly during rapid exploratory notebook prototyping. Must be eliminated before production deployment to avoid I/O bottlenecks and log bloat.
2. **Assert Statements**: Deployed as internal invariant contracts (e.g., `assert 0 <= normalized_val <= 1.0`, `assert len(clean_rows) <= len(raw_rows)`). In production, assertions can be disabled with `python -O` without degrading performance.
3. **The `logging` Module**: Production-grade diagnostic tracking configured with hierarchical levels (`DEBUG`, `INFO`, `WARNING`, `ERROR`, `CRITICAL`).
   - Allows redirection of high-verbosity traces to `cleaning_debug.log` while streaming concise progress to terminal console.
   - Central toggle: setting level to `logging.WARNING` instantly eliminates overhead in production.
4. **Interactive Debugger (`pdb`)**:
   - Invoked via `breakpoint()` at suspected failure points (e.g. malformed CSV parsing).
   - Allows runtime inspection of variable state (`p`), step execution (`n`, `s`), and stack inspection (`w`).

---

### A4.2: Performance Profiling Plan

1. **`time.perf_counter()` (Macro-level Benchmarking)**:
   - High-resolution wall-clock timer used to measure total batch execution time for 1,000, 100,000, and 1,000,000 rows.
2. **`timeit` Module (Micro-benchmarking)**:
   - Evaluates micro-optimizations, such as comparing list comprehension vs generator expression vs vectorised pandas expressions over 10,000 repetitions.
3. **`cProfile` (Deterministic CPU Profiling)**:
   - Invoked via `python -m cProfile -s tottime pipeline.py` or programmatically via `cProfile.Profile()`.
   - Generates detailed call counts, per-call time (`tottime`), and cumulative execution time (`cumtime`), pinpointing whether the bottleneck is string parsing, database write I/O, or mathematical scaling.
