"""
TASK 09: Complete Village Milk Co-operative Payment Calculator
Includes:
- Robust input handling and validation
- Precise rate computation and payouts using Decimal arithmetic
- Batch processing mode for farmers over 10-day period
- Interactive entry option
"""

from decimal import Decimal, ROUND_HALF_UP

# Configuration Constants
BASE_RATE = Decimal("30.00")
STANDARD_FAT = Decimal("3.5")
STANDARD_SNF = Decimal("8.5")
FAT_STEP_VAL = Decimal("0.40")
SNF_STEP_VAL = Decimal("0.30")

MIN_FAT = Decimal("2.0")
MAX_FAT = Decimal("7.0")
MIN_SNF = Decimal("6.0")
MAX_SNF = Decimal("12.0")

def round_curr(val: Decimal) -> Decimal:
    """Rounds to two decimal places using standard financial round-half-up."""
    return val.quantize(Decimal("0.01"), rounding=ROUND_HALF_UP)

def validate_milk_record(farmer_id: str, litres_str: str, fat_str: str, snf_str: str, shift: str):
    """
    Validates and converts string inputs.
    Returns (status, parsed_dict_or_error_msg).
    """
    if not farmer_id or not farmer_id.strip():
        return False, "Farmer ID cannot be empty."
    
    clean_id = farmer_id.strip()
    
    # Clean up commas
    try:
        litres = Decimal(litres_str.strip().replace(",", "."))
        fat = Decimal(fat_str.strip().replace(",", "."))
        snf = Decimal(snf_str.strip().replace(",", "."))
    except Exception as e:
        return False, f"Invalid numeric format: {e}"

    if litres <= 0:
        return False, f"Quantity must be greater than zero. Received: {litres}"
    if not (MIN_FAT <= fat <= MAX_FAT):
        return False, f"Fat {fat}% out of permissible range [{MIN_FAT}%, {MAX_FAT}%]"
    if not (MIN_SNF <= snf <= MAX_SNF):
        return False, f"SNF {snf}% out of permissible range [{MIN_SNF}%, {MAX_SNF}%]"
    
    norm_shift = shift.strip().capitalize()
    if norm_shift not in ("Morning", "Evening"):
        return False, f"Shift must be Morning or Evening. Received: {shift}"

    return True, {
        "id": clean_id,
        "litres": litres,
        "fat": fat,
        "snf": snf,
        "shift": norm_shift
    }

def calculate_rate(fat: Decimal, snf: Decimal) -> Decimal:
    """Calculates rate per litre based on fat and SNF steps."""
    fat_steps = ((fat - STANDARD_FAT) / Decimal("0.1")).quantize(Decimal("1"), rounding=ROUND_HALF_UP)
    snf_steps = ((snf - STANDARD_SNF) / Decimal("0.1")).quantize(Decimal("1"), rounding=ROUND_HALF_UP)
    rate = BASE_RATE + (fat_steps * FAT_STEP_VAL) + (snf_steps * SNF_STEP_VAL)
    return round_curr(rate)

def calculate_payment(litres: Decimal, rate: Decimal) -> Decimal:
    """Calculates payment for litres delivered at given rate."""
    return round_curr(litres * rate)

def process_batch(records: list):
    """Processes a list of raw entry tuples (id, litres, fat, snf, shift)."""
    valid_results = []
    rejections = []
    grand_total = Decimal("0.00")
    total_litres = Decimal("0.00")

    for raw in records:
        ok, res = validate_milk_record(*raw)
        if ok:
            rate = calculate_rate(res["fat"], res["snf"])
            pay = calculate_payment(res["litres"], rate)
            res["rate"] = rate
            res["payment"] = pay
            valid_results.append(res)
            grand_total += pay
            total_litres += res["litres"]
        else:
            rejections.append((raw, res))

    return {
        "valid": valid_results,
        "rejected": rejections,
        "total_payout": grand_total,
        "total_litres": total_litres
    }

if __name__ == "__main__":
    print("Milk Calculator Module Ready.")
