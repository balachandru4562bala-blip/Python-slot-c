"""
TASK 08: Algorithmic Hand Trace and Execution Demonstration
Runs the algorithm corresponding exactly to the ALGORITHM.md specification.
"""

def execute_algorithm():
    print("=" * 60)
    print("TASK 08: ALGORITHM EXECUTION & TRACE")
    print("=" * 60)

    entries = [
        {"id": "F101", "litres": 10.0, "fat": 3.5, "snf": 8.5, "shift": "Morning"},
        {"id": "F102", "litres": 8.5, "fat": 4.2, "snf": 8.7, "shift": "Evening"},
        {"id": "F103", "litres": 12.0, "fat": 3.1, "snf": 8.3, "shift": "Morning"},
    ]

    base_rate = 30.00
    fat_step_val = 0.40
    snf_step_val = 0.30
    running_total = 0.00

    print(f"{'Step':<5} | {'ID':<6} | {'Litres':<7} | {'Fat':<5} | {'SNF':<5} | {'FatSteps':<9} | {'SNFSteps':<9} | {'Rate':<7} | {'Payout':<8} | {'Running Total':<13}")
    print("-" * 95)

    for idx, e in enumerate(entries, 1):
        fat_diff = e["fat"] - 3.5
        fat_steps = round(fat_diff / 0.1)
        snf_diff = e["snf"] - 8.5
        snf_steps = round(snf_diff / 0.1)

        rate = base_rate + (fat_steps * fat_step_val) + (snf_steps * snf_step_val)
        payout = round(e["litres"] * rate, 2)
        running_total += payout

        print(f"{idx:<5} | {e['id']:<6} | {e['litres']:<7.1f} | {e['fat']:<5.1f} | {e['snf']:<5.1f} | {fat_steps:<9} | {snf_steps:<9} | {rate:<7.2f} | {payout:<8.2f} | Rs {running_total:<10.2f}")

    print("-" * 95)
    print(f"Final Ten-Day Total: Rs {running_total:.2f}")

if __name__ == "__main__":
    execute_algorithm()
