"""
ASSIGNMENT 2 - Q1: Decisions with Many Boundaries
State Electricity Subsidy Eligibility System

Rules:
- 100 units or less: Subsidy is given (Full Subsidy).
- 101 to 200 units: Partial subsidy ONLY if household holds a ration card.
- Above 200 units: No subsidy, UNLESS household has a member above 80 years of age (Senior Citizen Subsidy).
"""

# Implementation 1: Buggy Separate IF Statements
def subsidy_separate_ifs(units, has_ration_card, has_senior_citizen):
    """
    Demonstrates the bug of separate if statements:
    A household can match multiple independent if blocks, receiving multiple subsidies.
    """
    results = []
    if units <= 100:
        results.append("Full Subsidy (<= 100 units)")
    if 101 <= units <= 200 and has_ration_card:
        results.append("Partial Subsidy (101-200 units with Ration Card)")
    if units > 200 and has_senior_citizen:
        results.append("Senior Citizen Subsidy (> 200 units with Senior Member)")
    if units > 200 and not has_senior_citizen:
        results.append("No Subsidy")
    return results

# Implementation 2: Correct if-elif-else Decision Structure
def subsidy_if_elif_else(units, has_ration_card, has_senior_citizen):
    """
    Mutual exclusion guaranteed by if-elif-else chain.
    Exactly ONE decision is produced for any input.
    """
    if units <= 100:
        return "Full Subsidy"
    elif 101 <= units <= 200:
        if has_ration_card:
            return "Partial Subsidy"
        else:
            return "No Subsidy (No Ration Card)"
    else:  # units > 200
        if has_senior_citizen:
            return "Senior Citizen Subsidy"
        else:
            return "No Subsidy (> 200 units)"

# Alternative Concept 1: match-case (Python 3.10+) with guards
def subsidy_match_case(units, has_ration_card, has_senior_citizen):
    match units:
        case u if u <= 100:
            return "Full Subsidy"
        case u if 101 <= u <= 200 and has_ration_card:
            return "Partial Subsidy"
        case u if 101 <= u <= 200 and not has_ration_card:
            return "No Subsidy (No Ration Card)"
        case u if u > 200 and has_senior_citizen:
            return "Senior Citizen Subsidy"
        case _:
            return "No Subsidy (> 200 units)"

# Alternative Concept 2: Rule Table / Slab Search
SLABS = [
    # (upper_limit, condition_func, decision)
    (100, lambda card, sr: True, "Full Subsidy"),
    (200, lambda card, sr: card, "Partial Subsidy"),
    (200, lambda card, sr: not card, "No Subsidy (No Ration Card)"),
    (float('inf'), lambda card, sr: sr, "Senior Citizen Subsidy"),
    (float('inf'), lambda card, sr: not sr, "No Subsidy (> 200 units)")
]

def subsidy_rule_table(units, has_ration_card, has_senior_citizen):
    for upper_limit, condition, decision in SLABS:
        if units <= upper_limit and condition(has_ration_card, has_senior_citizen):
            return decision
    return "No Subsidy"

def run_q1_tests():
    print("=" * 70)
    print("ASSIGNMENT 2 - Q1: ELECTRICITY SUBSIDY BOUNDARY ANALYSIS")
    print("=" * 70)

    # 8 Test Households covering boundaries: 100, 101, 200, 201
    households = [
        {"name": "HH1 (Boundary 100)", "units": 100, "card": False, "sr": False, "expected": "Full Subsidy"},
        {"name": "HH2 (Boundary 101 with Card)", "units": 101, "card": True, "sr": False, "expected": "Partial Subsidy"},
        {"name": "HH3 (Boundary 101 no Card)", "units": 101, "card": False, "sr": False, "expected": "No Subsidy (No Ration Card)"},
        {"name": "HH4 (Interior 150 with Card)", "units": 150, "card": True, "sr": False, "expected": "Partial Subsidy"},
        {"name": "HH5 (Boundary 200 with Card)", "units": 200, "card": True, "sr": False, "expected": "Partial Subsidy"},
        {"name": "HH6 (Boundary 201 with Senior)", "units": 201, "card": False, "sr": True, "expected": "Senior Citizen Subsidy"},
        {"name": "HH7 (Boundary 201 no Senior)", "units": 201, "card": True, "sr": False, "expected": "No Subsidy (> 200 units)"},
        {"name": "HH8 (Boundary 0 units)", "units": 0, "card": False, "sr": False, "expected": "Full Subsidy"},
    ]

    print(f"\n{'Household':<28} | {'Units':<6} | {'Card':<6} | {'Senior':<6} | {'Separate IFs':<35} | {'if-elif-else Decision':<25}")
    print("-" * 115)

    for hh in households:
        sep_res = subsidy_separate_ifs(hh["units"], hh["card"], hh["sr"])
        correct_res = subsidy_if_elif_else(hh["units"], hh["card"], hh["sr"])
        match_res = subsidy_match_case(hh["units"], hh["card"], hh["sr"])
        table_res = subsidy_rule_table(hh["units"], hh["card"], hh["sr"])

        sep_str = "; ".join(sep_res) if sep_res else "None"
        print(f"{hh['name']:<28} | {hh['units']:<6} | {str(hh['card']):<6} | {str(hh['sr']):<6} | {sep_str:<35} | {correct_res:<25}")

        # Assert consistency
        assert correct_res.startswith(hh["expected"].split()[0]), f"Mismatch for {hh['name']}"
        assert match_res == correct_res
        assert table_res == correct_res

    print("\n[PASS] All 8 boundary households verified across all decision structures.")
    print("\n--- Design Defense: Nested IF vs Combined Boolean ---")
    print("Combined boolean (`if units <= 100: ... elif 101 <= units <= 200 and has_ration_card: ...`)")
    print("clearly partitions the unit slabs first, preventing logical overlap and ensuring single decision delivery.")

if __name__ == "__main__":
    run_q1_tests()
