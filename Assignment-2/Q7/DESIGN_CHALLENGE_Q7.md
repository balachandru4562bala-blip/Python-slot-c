# ASSIGNMENT 2 - Q7: DAY-4 DESIGN CHALLENGE
## Diagnose, Redesign, and Validate: Temple Step Climbing Combinatorics

---

### Part A: Diagnose the Bottleneck (2 Marks)
In Q6, two primary bottlenecks were observed as input size $n$ scaled:
1. **Exponential Work in Plain Recursion (`ways_naive`)**:
   - The recursive call tree generates $2 \times \text{Fib}(n+1) - 1$ total function calls.
   - For $n = 25$, 242,785 function calls were executed to compute a value of 121,393.
   - At $n = 50$, the required function calls exceed $4.07 \times 10^{10}$, taking hours.
2. **Call-Stack Exhaustion in Memoised Recursion (`ways_memo`)**:
   - Although `@lru_cache` reduces time complexity to $O(n)$, it retains the top-down recursive descent architecture.
   - For $n = 1000$, CPython allocates 1,000 consecutive stack frames, triggering `RecursionError: maximum recursion depth exceeded`.
   - Furthermore, memoisation retains an internal dictionary of 1,000 key-value mappings, consuming unnecessary heap memory.

---

### Part B: Define the Design Objective (2 Marks)
The measurable objectives for the redesigned system are:
1. **Eliminate Stack Exhaustion**: Support step counts up to $n = 100,000$ with **zero stack frame allocation** and zero risk of `RecursionError`.
2. **Strict Auxiliary Memory Bound**: Reduce auxiliary space complexity from $O(n)$ stack/cache to **strict $O(1)$ constant memory**.
3. **Execution Latency**: Compute $ways(1000)$ in **less than 0.5 milliseconds** ($< 0.0005$ s).
4. **Logarithmic Scaling Option**: Implement fast matrix exponentiation achieving $O(\log n)$ time complexity for ultra-large architectural scales ($n \ge 100,000$).

---

### Part C: Design the Revised Solution (4 Marks)
The recurrence relation satisfies:
$$\text{ways}(n) = \text{ways}(n-1) + \text{ways}(n-2)$$

#### Solution 1: Bottom-Up Space-Optimised Iterative Dynamic Programming
Instead of maintaining the entire history of $n$ subproblems, only the preceding two values ($prev_2$ and $prev_1$) are required to compute the next value.
```text
ALGORITHM WaysIterative(n)
START
    IF n <= 1 THEN
        RETURN 1
    ENDIF
    SET prev2 TO 1
    SET prev1 TO 1
    FOR step FROM 2 TO n DO
        SET curr TO prev1 + prev2
        SET prev2 TO prev1
        SET prev1 TO curr
    ENDFOR
    RETURN prev1
END
```
- **Time Complexity**: $O(n)$ single-pass loop.
- **Space Complexity**: $O(1)$ auxiliary variables.

#### Solution 2: Binary Matrix Exponentiation
Using transition matrix multiplication:
$$\begin{pmatrix} \text{ways}(n) \\ \text{ways}(n-1) \end{pmatrix} = \begin{pmatrix} 1 & 1 \\ 1 & 0 \end{pmatrix}^{n-1} \begin{pmatrix} 1 \\ 1 \end{pmatrix}$$
Using repeated squaring (binary exponentiation), the matrix power is computed in $O(\log n)$ matrix multiplications.

---

### Part D: Predict Before Implementing (1 Mark)
1. At $n = 1000$, the iterative solution will execute without errors in $< 0.1$ ms with $O(1)$ auxiliary space.
2. At $n = 10,000$, the matrix exponentiation algorithm will perform only $\approx \log_2(10000) \approx 14$ matrix multiplications, demonstrating asymptotic superiority over linear loops.

---

### Part E & F: Implementation, Validation & Defense (4 Marks)
See `redesign_steps_challenge.py` for comparative timings, memory measurements, and defense.
