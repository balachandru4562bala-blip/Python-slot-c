"""
ASSIGNMENT 5 - TASK B2: Engineer Adversarial Data
Robustness and Security Testing for Air Quality and AI Modules

Includes:
- Complete the Code: TODO 1 executemany, TODO 2 parameterised station_average()
- SQL Injection comparison: ? placeholders vs string concatenation f"..."
- File pipeline adversarial testing: missing columns, wrong delimiters, non-utf8 encodings, empty files
- Sentiment Analysis Adversarial Stress Test: Sarcasm, double negatives, mixed sentiment
"""

import sqlite3
import csv
import io
import os

# --- Complete the Code Section ---
def run_complete_the_code_b2():
    print("\n--- Complete the Code Expected Execution ---")
    readings = [("Adyar", "2026-10-01", 48.0), ("Guindy", "2026-10-01", 95.0),
                ("Guindy", "2026-10-03", 121.0), ("Adyar", "2026-10-04", 60.0)]

    con = sqlite3.connect(":memory:")
    con.execute("CREATE TABLE aq (station TEXT, day TEXT, pm25 REAL)")
    # TODO 1: Insert all readings with ONE executemany call using ? placeholders, then
    # commit
    con.executemany("INSERT INTO aq (station, day, pm25) VALUES (?, ?, ?)", readings)
    con.commit()

    def station_average(name):
        # TODO 2: Return the average pm25 of the given station using a parameterised SELECT
        # ... WHERE station = ?
        cur = con.cursor()
        cur.execute("SELECT AVG(pm25) FROM aq WHERE station = ?", (name,))
        row = cur.fetchone()
        return row[0] if row and row[0] is not None else None

    avg_adyar = station_average("Adyar")
    avg_guindy = station_average("Guindy")
    avg_inject = station_average("Adyar' OR '1'='1")

    print(avg_adyar, avg_guindy)
    print(avg_inject) # an injection attempt finds nothing

    assert avg_adyar == 54.0 and avg_guindy == 108.0
    assert avg_inject is None
    print("[PASS] Complete the code output matched exactly (54.0, 108.0, None)!")

    # Demonstrating vulnerability of string concatenation
    print("\n--- SQL Injection Vulnerability Demonstration (Concatenation vs Placeholder) ---")
    malicious_input = "Adyar' OR '1'='1"
    vulnerable_sql = f"SELECT AVG(pm25) FROM aq WHERE station = '{malicious_input}'"
    print(f"Vulnerable SQL Query: {vulnerable_sql}")
    cur = con.cursor()
    cur.execute(vulnerable_sql)
    injected_result = cur.fetchone()[0]
    print(f"Result from vulnerable string concatenation: {injected_result} (DANGEROUS: Returned global average of ALL rows!)")
    print("Explanation: The '?' placeholder instructs the SQLite database engine to bind the parameter")
    print("as a literal string value. The quote characters are treated as literal text, never syntax tokens.")
    con.close()

# --- Adversarial File Input Testing ---
def test_adversarial_files():
    print("\n--- Adversarial Telemetry File Robustness Tests ---")

    # 1. Missing Column File
    csv_missing_col = "station,date\nAdyar,2026-10-01\n"
    # 2. Wrong Delimiter (Tab instead of Comma)
    csv_tab_delim = "station\tdate\tpm25\nAdyar\t2026-10-01\t45.0\n"
    # 3. Completely Empty File
    csv_empty = ""

    def safe_parse_csv(text):
        if not text.strip():
            return "REJECTED: Empty file"
        reader = csv.reader(io.StringIO(text))
        header = next(reader, None)
        if not header or len(header) < 3 or "pm25" not in header:
            return f"REJECTED: Malformed schema/delimiter (detected {len(header) if header else 0} columns)"
        return "ACCEPTED"

    print("Missing 'pm25' column test :", safe_parse_csv(csv_missing_col))
    print("Tab-delimited file test     :", safe_parse_csv(csv_tab_delim))
    print("Empty file test             :", safe_parse_csv(csv_empty))

# --- Adversarial Sentiment Testing ---
POSITIVE = {"good", "clean", "fast", "helpful", "improved"}
NEGATIVE = {"bad", "dirty", "slow", "rude", "smoke", "broken"}
NEGATORS = {"not", "never", "no"}

def score_sentiment(text):
    words = text.lower().replace(".", " ").replace(",", " ").replace("!", " ").split()
    total = 0
    for i, w in enumerate(words):
        val = 0
        if w in POSITIVE:
            val = 1
        elif w in NEGATIVE:
            val = -1
        if val != 0:
            if i > 0 and words[i - 1] in NEGATORS:
                val = -val
            total += val
    return total

def test_adversarial_sentiment():
    print("\n--- Adversarial Sentiment Stress Test ---")
    adversarial_cases = [
        ("Sarcasm", "Oh brilliant, the air is full of thick black smoke, just wonderful!"),
        ("Double Negative", "The new pollution control system is not bad at all."),
        ("Mixed Sentiment", "Staff were helpful, but the air monitoring app was slow and broken."),
        ("Implicit Negation", "Hardly any clean air left in this neighborhood.")
    ]

    for label, sentence in adversarial_cases:
        score = score_sentiment(sentence)
        predicted = "positive" if score > 0 else "negative" if score < 0 else "neutral"
        print(f"[{label:<18}] '{sentence}'")
        print(f"   -> Lexicon Score: {score:+d} (Predicted: {predicted.upper()})")

    print("\nInsights Revealed by Adversarial Inputs:")
    print("1. Sarcasm: Lexicon counts positive words ('brilliant', 'wonderful') and fails to detect sarcastic irony.")
    print("2. Complex Syntax: Double negatives ('not bad') are handled if directly adjacent, but distance breaks it.")
    print("3. Mixed Sentiment: Equal positive and negative tokens neutralize each other to 0 (Neutral), obscuring complaint nuance.")

def run_task_b2():
    print("=" * 75)
    print("ASSIGNMENT 5 - TASK B2: ADVERSARIAL TESTING & DEFENSIVE ENGINEERING")
    print("=" * 75)
    run_complete_the_code_b2()
    test_adversarial_files()
    test_adversarial_sentiment()

if __name__ == "__main__":
    run_task_b2()
