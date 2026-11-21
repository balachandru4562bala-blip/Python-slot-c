"""
TASK 12: Day-4 Design Challenge - Adapted Co-operative Payment Calculator
Handles:
1. High-precision 2-decimal Analyser readings (e.g. 4.25% fat, 8.63% snf)
2. Seasonal rates: Summer (April-June) vs Regular (Other months)
3. Volume bonus: > 500 L in 10 days earns Rs 0.50 / L bonus on ALL litres
"""

from decimal import Decimal, ROUND_HALF_UP

# --- Rate Profiles ---
SEASON_SUMMER = {
    "name": "Summer (Apr-Jun)",
    "base_rate": Decimal("32.00"),
    "fat_step_val": Decimal("0.45"),
    "snf_step_val": Decimal("0.30"),
}

SEASON_REGULAR = {
    "name": "Regular (Jul-Mar)",
    "base_rate": Decimal("30.00"),
    "fat_step_val": Decimal("0.40"),
    "snf_step_val": Decimal("0.30"),
}

STANDARD_FAT = Decimal("3.5")
STANDARD_SNF = Decimal("8.5")
BONUS_THRESHOLD_LITRES = Decimal("500.0")
BONUS_RATE_PER_LITRE = Decimal("0.50")

def get_rate_card(month: int) -> dict:
    """Returns the seasonal rate profile based on calendar month (1-12)."""
    if month in (4, 5, 6):
        return SEASON_SUMMER
    return SEASON_REGULAR

def calculate_rate_adapted(fat: Decimal, snf: Decimal, month: int) -> Decimal:
    """
    Computes rate per litre handling 2-decimal readings and seasonal rules.
    Steps are rounded to nearest whole 0.1% step using ROUND_HALF_UP.
    """
    rate_card = get_rate_card(month)
    # Fat steps
    fat_diff = fat - STANDARD_FAT
    fat_steps = (fat_diff / Decimal("0.1")).quantize(Decimal("1"), rounding=ROUND_HALF_UP)
    
    # SNF steps
    snf_diff = snf - STANDARD_SNF
    snf_steps = (snf_diff / Decimal("0.1")).quantize(Decimal("1"), rounding=ROUND_HALF_UP)
    
    rate = rate_card["base_rate"] + (fat_steps * rate_card["fat_step_val"]) + (snf_steps * rate_card["snf_step_val"])
    return rate.quantize(Decimal("0.01"), rounding=ROUND_HALF_UP)

def calculate_entry_payout(litres: Decimal, fat: Decimal, snf: Decimal, month: int) -> Decimal:
    """Calculates payout for a single shift delivery."""
    rate = calculate_rate_adapted(fat, snf, month)
    return (litres * rate).quantize(Decimal("0.01"), rounding=ROUND_HALF_UP)

def calculate_ten_day_bill(entries: list, month: int) -> dict:
    """
    Computes 10-day bill for a farmer, applying seasonal rates and volume bonus.
    entries: list of (litres, fat, snf)
    """
    total_litres = Decimal("0.00")
    base_payout = Decimal("0.00")
    detailed_lines = []
    
    for l, f, s in entries:
        l_d = Decimal(str(l))
        f_d = Decimal(str(f))
        s_d = Decimal(str(s))
        
        rate = calculate_rate_adapted(f_d, s_d, month)
        pay = (l_d * rate).quantize(Decimal("0.01"), rounding=ROUND_HALF_UP)
        
        detailed_lines.append({
            "litres": l_d,
            "fat": f_d,
            "snf": s_d,
            "rate": rate,
            "payout": pay
        })
        total_litres += l_d
        base_payout += pay

    # Volume Bonus check: STRICTLY GREATER THAN 500 Litres
    qualifies_for_bonus = total_litres > BONUS_THRESHOLD_LITRES
    if qualifies_for_bonus:
        bonus_amount = (total_litres * BONUS_RATE_PER_LITRE).quantize(Decimal("0.01"), rounding=ROUND_HALF_UP)
    else:
        bonus_amount = Decimal("0.00")

    final_total = base_payout + bonus_amount

    return {
        "month": month,
        "season": get_rate_card(month)["name"],
        "total_litres": total_litres,
        "base_payout": base_payout,
        "qualifies_bonus": qualifies_for_bonus,
        "bonus_amount": bonus_amount,
        "final_total": final_total,
        "lines": detailed_lines
    }
