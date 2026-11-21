# TASK 12: Day-4 Design Challenge — Re-evaluate and Adapt the Design

## Part A: Impact Analysis (2 Marks)
The milk co-operative introduced three major operational revisions:
1. **High-Precision Analyser Readings**: The automated analyser outputs Fat and SNF to **two decimal places** (e.g., 4.25% Fat, 8.63% SNF).
   - *Impact*: In the original design, readings had one decimal place (e.g., 4.2%). With two decimals, $(4.25 - 3.5) / 0.1 = 7.5$ steps. A decision must be made regarding fractional steps: does the cooperative use standard round-half-up (rounding 7.5 to 8 steps), or pro-rata linear interpolation ($7.5 \times 0.40 = 3.00$)? Under the cooperative rule of "Every 0.1% fat adds/subtracts...", rounding to the nearest whole 0.1% step or continuous proportional evaluation must be standardized. Using `ROUND_HALF_UP` on $((fat - 3.5)/0.1)$ rounds 7.5 to 8 steps.
2. **Seasonal Rate Structures**:
   - **Summer Season (April to June)**: Base Rate = Rs 32.00, Fat Step = Rs 0.45, SNF Step = Rs 0.30.
   - **Regular Season (July to March)**: Base Rate = Rs 30.00, Fat Step = Rs 0.40, SNF Step = Rs 0.30.
   - *Impact*: Static constants in a single module fail because rates are month-dependent. The calculator must accept `month` or `season` parameter.
3. **Volume Incentive Bonus**:
   - Deliveries $> 500$ litres in a 10-day cycle qualify for a retrospective **Rs 0.50/L bonus on all litres**.
   - Exactly 500 litres earns **no bonus**.
   - *Impact*: Payout cannot be computed purely per-shift in isolation; a final aggregation pass at the end of the 10-day cycle must verify the total volume and apply the retrospective bonus.

---

## Part B: Evaluation of the Original Design (2 Marks)
- **Verdict**: **MODIFY** the original design.
- The original design assumed static global constants and single-transaction independence. 
- Retaining the original design fails completely on seasonal transitions and volume bonuses.
- A full ground-up rewrite is unnecessary because the core mathematical principle (step-based adjustment with Decimal monetary precision) remains sound and proven.
- Hence, the original design is modified into a state-aware, seasonal-capable architecture.

---

## Part C: Revised Architecture Specification (2 Marks)
- Rate cards defined as seasonal profiles: `SEASON_SUMMER` (April–June) and `SEASON_REGULAR` (Other months).
- Added `get_rate_card(month: int)` to return active parameters dynamically.
- Step calculation updated to handle 2-decimal inputs with configurable rounding policies.
- Added `calculate_ten_day_farmer_bill(entries, month)` to track 10-day cumulative litres and apply the $> 500$ L volume bonus.

---

## Part D: Evidence-Based Defence & Verification (2 Marks)
See `test_adapted_calculator.py` for full test execution across:
- Season 1 (May - Summer) vs Season 2 (October - Regular)
- 2-decimal step resolution (4.25% fat, 8.63% snf)
- Volume bonus boundary conditions:
  - 499.9 Litres -> No bonus
  - 500.0 Litres -> No bonus (Strictly greater than 500 required)
  - 500.1 Litres -> Qualifies for Rs 0.50 * 500.1 = Rs 250.05 bonus
