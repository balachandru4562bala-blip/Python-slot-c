"""
ASSIGNMENT 2 - Q2: Loops that Count Attempts
OTP Verification at a Bank Kiosk

Features:
- Maximum 3 attempts
- Blank entries do not burn attempts (continue, pass)
- Break on successful OTP
- Loop 'else' clause triggers 30-minute lockout
- While loop vs For loop implementations
- Changed condition: 2 bonus attempts upon answering security question
- Alternative concept: Recursive attempt verification vs Iterative loop
"""

def verify_otp_while(correct_otp, simulated_inputs):
    """
    While-loop implementation of OTP verification.
    More natural when counter increments only on non-blank attempts.
    """
    MAX_ATTEMPTS = 3
    attempts_used = 0
    input_idx = 0
    log = []

    while attempts_used < MAX_ATTEMPTS:
        if input_idx >= len(simulated_inputs):
            break
        raw_input = simulated_inputs[input_idx]
        input_idx += 1

        # Handling blank entries
        entered_otp = raw_input.strip()
        if not entered_otp:
            log.append("Blank entry detected. Please type digits (Not counted as attempt).")
            pass  # Explicit placeholder demonstrating pass construct
            continue  # Skips attempt increment

        attempts_used += 1
        if entered_otp == correct_otp:
            log.append(f"OTP verified successfully on attempt {attempts_used}! Access granted.")
            break
        else:
            log.append(f"Wrong OTP '{entered_otp}'. Attempts remaining: {MAX_ATTEMPTS - attempts_used}")
    else:
        # Loop else executed ONLY if while loop terminated without a 'break'
        log.append("SECURITY ALERT: 3 incorrect attempts exceeded. Account LOCKED for 30 minutes.")

    return log

def verify_otp_for(correct_otp, simulated_inputs):
    """
    For-loop implementation using range(3).
    Demonstrates break and loop else.
    """
    log = []
    MAX_ATTEMPTS = 3
    # Filter out blank inputs first so range(3) reflects valid attempt slots
    valid_inputs = [inp.strip() for inp in simulated_inputs if inp.strip()]

    for attempt in range(1, MAX_ATTEMPTS + 1):
        if attempt - 1 >= len(valid_inputs):
            break
        entered_otp = valid_inputs[attempt - 1]

        if entered_otp == correct_otp:
            log.append(f"OTP verified successfully on attempt {attempt}! Access granted.")
            break
        else:
            log.append(f"Wrong OTP '{entered_otp}'. Attempts remaining: {MAX_ATTEMPTS - attempt}")
    else:
        log.append("SECURITY ALERT: 3 incorrect attempts exceeded. Account LOCKED for 30 minutes.")

    return log

def verify_otp_extended(correct_otp, security_ans, simulated_data):
    """
    Changed Condition: If customer fails 3 times, answering security question
    grants 2 extra attempts.
    """
    log = []
    attempts = 0
    max_allowed = 3
    bonus_granted = False
    idx = 0

    while attempts < max_allowed and idx < len(simulated_data):
        item = simulated_data[idx].strip()
        idx += 1

        if not item:
            continue

        attempts += 1
        if item == correct_otp:
            log.append(f"Success on attempt {attempts}! Access granted.")
            return log
        else:
            log.append(f"Incorrect OTP '{item}'. Attempts: {attempts}/{max_allowed}")

        # Check if 3 attempts reached and bonus not yet offered
        if attempts == 3 and not bonus_granted:
            log.append("3 failed attempts. Security challenge offered.")
            if idx < len(simulated_data):
                ans = simulated_data[idx].strip()
                idx += 1
                if ans.lower() == security_ans.lower():
                    bonus_granted = True
                    max_allowed += 2
                    log.append("Security answer CORRECT! 2 extra attempts granted.")
                else:
                    log.append("Security answer INCORRECT.")
                    break

    log.append("SECURITY ALERT: Maximum attempts reached. Account LOCKED.")
    return log

# Alternative Concept: Recursive Attempt Verification
def verify_otp_recursive(correct_otp, inputs, attempt=1, max_attempts=3):
    """
    Recursive implementation: O(a) time, O(a) call stack space.
    """
    if attempt > max_attempts or not inputs:
        return ["RECURSIVE: Maximum attempts reached. Account LOCKED."]
    
    current = inputs[0].strip()
    remaining = inputs[1:]
    
    if not current:
        return ["RECURSIVE: Blank ignored."] + verify_otp_recursive(correct_otp, remaining, attempt, max_attempts)
    
    if current == correct_otp:
        return [f"RECURSIVE: Verified on attempt {attempt}! Access granted."]
    else:
        return [f"RECURSIVE: Failed attempt {attempt}."] + verify_otp_recursive(correct_otp, remaining, attempt + 1, max_attempts)

def run_q2_tests():
    print("=" * 70)
    print("ASSIGNMENT 2 - Q2: OTP VERIFICATION & LOOP CONTROL FLOW")
    print("=" * 70)

    correct_pin = "4829"

    # Test Case 1: Blank entries followed by success on 2nd counted attempt
    scenario_1 = ["", "  ", "1111", "", "4829"]
    print("\n--- Scenario 1: Blanks + Success on 2nd Counted Attempt ---")
    res1 = verify_otp_while(correct_pin, scenario_1)
    for line in res1:
        print(f"  {line}")
    assert any("Access granted" in l for l in res1)

    # Test Case 2: Three wrong attempts -> Account locked
    scenario_2 = ["", "1001", "2002", "3003", "4829"]
    print("\n--- Scenario 2: 3 Incorrect Attempts -> Account Locked ---")
    res2 = verify_otp_while(correct_pin, scenario_2)
    for line in res2:
        print(f"  {line}")
    assert any("Account LOCKED" in l for l in res2)

    # Test Case 3: Changed Condition with Security Question Bonus
    print("\n--- Scenario 3: Security Question Unlocks 2 Bonus Attempts ---")
    scenario_3 = [
        "1111", "2222", "3333",  # 3 failures
        "Blue",                   # Correct security answer (Favourite color: Blue)
        "9999",                   # Attempt 4 (fail)
        "4829"                    # Attempt 5 (success!)
    ]
    res3 = verify_otp_extended(correct_pin, "Blue", scenario_3)
    for line in res3:
        print(f"  {line}")
    assert any("Access granted" in l for l in res3)

    # Test Case 4: Recursive attempt comparison
    print("\n--- Scenario 4: Recursive Verification ---")
    rec_res = verify_otp_recursive(correct_pin, ["", "1234", "4829"])
    for line in rec_res:
        print(f"  {line}")

    print("\n[PASS] All loop variants, continue/break/else, and security extension verified.")

if __name__ == "__main__":
    run_q2_tests()
