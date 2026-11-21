"""
ASSIGNMENT 5 - TASK B4: Final Engineering Decision & AI Applications
Citizen Complaints Analytics & High-Frequency Telemetry Scaling

Includes:
- Complete the Code: TODO 1 in score(text) with negation flipping
- Evaluation of Sentiment Scorer and Extractive Summariser on 50 real-world citizen complaints
- Measurement of Human-Model Agreement Rate (%)
- Database Indexing Benchmark: Evaluating index acceleration on (station, reading_date)
- Conversational Rule-Based Chatbot querying the SQLite database
- Production architectural decision for scaling to 100 stations at 15-min frequency (~35M rows/year)
"""

import sqlite3
import time
import os
from collections import Counter

CURRENT_DIR = os.path.dirname(os.path.abspath(__file__))
DB_PATH = os.path.join(CURRENT_DIR, "..", "..", "database", "air_quality.db")

# --- Complete the Code Section ---
POSITIVE = {"good", "clean", "fast", "helpful", "improved"}
NEGATIVE = {"bad", "dirty", "slow", "rude", "smoke", "broken"}
NEGATORS = {"not", "never", "no"}

def score(text):
    """+1 per positive word, -1 per negative word; a preceding negator flips it."""
    words = text.lower().replace(".", " ").replace(",", " ").split()
    total = 0
    # TODO 1: For each word, find its value (+1, -1 or 0); if the previous word is a
    # negator, flip the sign; add it to total
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

def label(text):
    s = score(text)
    return "positive" if s > 0 else "negative" if s < 0 else "neutral"

# --- Extractive Summariser Implementation ---
STOPWORDS = {"is", "the", "and", "of", "to", "in", "a", "for", "on", "with", "at", "by", "from", "are", "was", "were", "this", "that"}

def extractive_summarise(text, top_k_sentences=2):
    sentences = [s.strip() for s in text.replace("\n", " ").split(".") if s.strip()]
    if len(sentences) <= top_k_sentences:
        return ". ".join(sentences) + "."
    
    # Calculate word frequency weights
    words = [w.lower().strip(".,!?:;\"'") for s in sentences for w in s.split()]
    filtered_words = [w for w in words if w not in STOPWORDS and len(w) > 2]
    freq = Counter(filtered_words)
    
    # Score sentences
    sentence_scores = []
    for idx, s in enumerate(sentences):
        s_words = [w.lower().strip(".,!?:;\"'") for w in s.split()]
        score_val = sum(freq.get(w, 0) for w in s_words)
        sentence_scores.append((idx, score_val, s))
        
    # Pick top k preserving original sequence
    top_sentences = sorted(sentence_scores, key=lambda x: -x[1])[:top_k_sentences]
    top_sentences.sort(key=lambda x: x[0])  # Restore order
    return ". ".join(s for _, _, s in top_sentences) + "."

# --- 50 Citizen Complaints Dataset ---
SAMPLE_50_COMPLAINTS = [
    ("Heavy smoke from industrial chimneys near Manali, throat is burning.", "negative"),
    ("Roads are clean and the bus service was fast this morning.", "positive"),
    ("Not bad at all, the waste collection has improved significantly.", "positive"),
    ("Garbage burning near the railway track, air is dirty and foul.", "negative"),
    ("The mobile application was slow, but customer support staff were helpful.", "neutral"), # Mixed
    ("Pollution control board staff were not helpful when we called to report.", "negative"),
    ("Parks in Anna Nagar are clean and pleasant for morning walkers.", "positive"),
    ("Air quality in Velachery is extremely bad today due to heavy traffic.", "negative"),
    ("Prompt action by municipality, smoke issue was resolved quickly.", "positive"),
    ("Continuous toxic smell from chemical plant, our children are coughing.", "negative"),
    ("Never clean, the streets are permanently covered in construction dust.", "negative"),
    ("Bus frequency has improved and diesel smoke has noticeably reduced.", "positive"),
    ("App server is broken and shows error 500 continuously.", "negative"),
    ("The staff were rude and refused to log our noise pollution grievance.", "negative"),
    ("Good initiative to monitor particulate matter in residential colonies.", "positive"),
    ("Diesel generator smoke from commercial complex entering our apartments.", "negative"),
    ("Clean green corridor in Guindy national park, very fresh air.", "positive"),
    ("Not clean, drainage overflow on main junction causing stench.", "negative"),
    ("Fast resolution of burning garbage complaint within two hours.", "positive"),
    ("Air is terrible, visibility dropped drastically near bypass road.", "negative"),
    ("Solar air quality display screen in Koyambedu is broken and dark.", "negative"),
    ("Traffic police are helpful in diverting vehicles to curb congestion.", "positive"),
    ("High soot deposition on our terrace, air is very dirty.", "negative"),
    ("No smoke detected today, weather is clear and breezy.", "positive"),
    ("Public transport fleet has improved with new electric buses.", "positive"),
    ("Trucks emitting dark black smoke without PUC emission certificates.", "negative"),
    ("Pavement cleaning drive was completed fast, footpath is neat.", "positive"),
    ("Smog is bad, eyes are stinging while driving two-wheeler.", "negative"),
    ("Staff was not rude, they explained the AQI parameters patiently.", "positive"),
    ("Waste dumping site caught fire, suffocating smoke spreading all over.", "negative"),
    ("Air monitoring sensor was repaired fast, readings are back online.", "positive"),
    ("Dirty storm water drain emitting unbearable gas odor.", "negative"),
    ("Green tree planting drive has improved neighborhood environment.", "positive"),
    ("Unregulated construction work generating massive clouds of fine sand dust.", "negative"),
    ("Complaints portal is fast, received SMS confirmation in minutes.", "positive"),
    ("Air quality near hospital is bad, patients are facing breathing issues.", "negative"),
    ("The inspection officer was helpful and issued notice to the polluter.", "positive"),
    ("Factory sirens are loud and chimney emission is dark grey smoke.", "negative"),
    ("Clean lake surrounding with walking track, great civic improvement.", "positive"),
    ("Not helpful service, automated helpline repeats generic recording.", "negative"),
    ("Cycle tracks in Besant Nagar are well maintained and clean.", "positive"),
    ("Open burning of dry leaves in community park creates heavy smoke.", "negative"),
    ("Sanitation workers did a good job clearing roadside debris.", "positive"),
    ("Unpaved road margins kicking up dust, visibility is poor.", "negative"),
    ("Very good initiative by pollution control board to release open data.", "positive"),
    ("Chemical tanker leaking pungent gas, citizens feel dizzy.", "negative"),
    ("New emission norms have improved air clarity over city center.", "positive"),
    ("Slow grievance portal takes 10 minutes to submit a single photo.", "negative"),
    ("Staff was polite and helpful during our field inspection visit.", "positive"),
    ("Heavy smoke from brick kilns on city outskirts polluting farmland.", "negative"),
]

def evaluate_complaints_sentiment():
    print("\n--- Evaluating Lexicon Scorer on 50 Real-World Citizen Complaints ---")
    correct_matches = 0
    mismatches = []
    
    for idx, (text, human_label) in enumerate(SAMPLE_50_COMPLAINTS, 1):
        pred_label = label(text)
        is_agree = (pred_label == human_label)
        if is_agree:
            correct_matches += 1
        else:
            mismatches.append((idx, text, human_label, pred_label))
            
    accuracy_pct = (correct_matches / len(SAMPLE_50_COMPLAINTS)) * 100.0
    print(f"Total Complaints Evaluated    : {len(SAMPLE_50_COMPLAINTS)}")
    print(f"Human-Model Agreement Count   : {correct_matches}")
    print(f"Agreement Rate Percentage     : {accuracy_pct:.1f}%")

    if mismatches:
        print("\nSample Mismatches (Where Rule-Based Lexicon Failed):")
        for idx, txt, human, pred in mismatches[:4]:
            print(f"  #{idx}: '{txt}'")
            print(f"       Human Label: {human.upper()} | Model Predicted: {pred.upper()}")

# --- Rule-Based Conversational Chatbot ---
def chatbot_query(user_prompt, con):
    """
    Rule-based chatbot extracting intent and querying SQLite database.
    """
    prompt = user_prompt.lower().strip()
    cur = con.cursor()
    
    # Intent 1: Check PM2.5 for a specific station
    stations = ["adyar", "guindy", "royapuram", "velachery", "t. nagar", "anna nagar",
                "alandur", "manali", "kodambakkam", "ambattur", "perambur", "tambaram"]
    
    matched_station = None
    for st in stations:
        if st in prompt:
            matched_station = st.title()
            break
            
    if "pm25" in prompt or "pm2.5" in prompt or "air quality" in prompt or "pollution" in prompt:
        if matched_station:
            cur.execute("""
            SELECT pm25, temperature, reading_date, hour
            FROM readings WHERE station = ?
            ORDER BY reading_date DESC, hour DESC LIMIT 1
            """, (matched_station,))
            res = cur.fetchone()
            if res:
                aqi_level = "Satisfactory" if res[0] <= 60 else "Moderate" if res[0] <= 90 else "Poor"
                return f"At {matched_station} on {res[2]} (Hour {res[3]}:00), the PM2.5 is {res[0]} ug/m3 with temperature {res[1]} C. Air quality is currently {aqi_level}."
            return f"No recent telemetry found for station '{matched_station}'."
        else:
            cur.execute("SELECT station, ROUND(AVG(pm25), 1) FROM readings GROUP BY station ORDER BY AVG(pm25) ASC LIMIT 1")
            cleanest = cur.fetchone()
            return f"Please specify a station. Currently, the cleanest monitored station is {cleanest[0]} with average PM2.5 of {cleanest[1]} ug/m3."

    # Intent 2: List stations
    if "station" in prompt or "locations" in prompt:
        cur.execute("SELECT DISTINCT station FROM readings")
        all_st = [r[0] for r in cur.fetchall()]
        return f"The monitoring network tracks 12 stations: {', '.join(all_st)}."

    # Default fallback
    return "I am the City Air Quality Assistant. Ask me: 'What is the PM2.5 in Adyar?' or 'Which stations are monitored?'"

# --- Database Index Performance Benchmark ---
def benchmark_database_index(con):
    print("\n--- B4.2: Database Index Acceleration Benchmark ---")
    cur = con.cursor()
    
    # 1. Drop index to benchmark unindexed table scan
    cur.execute("DROP INDEX IF EXISTS idx_station_date")
    
    t0 = time.perf_counter()
    for _ in range(200):
        cur.execute("SELECT AVG(pm25) FROM readings WHERE station = 'Adyar' AND reading_date = '2026-10-15'")
        _ = cur.fetchall()
    t_unindexed = time.perf_counter() - t0
    
    # 2. Add composite B-Tree index on (station, reading_date)
    cur.execute("CREATE INDEX idx_station_date ON readings(station, reading_date)")
    con.commit()
    
    t0 = time.perf_counter()
    for _ in range(200):
        cur.execute("SELECT AVG(pm25) FROM readings WHERE station = 'Adyar' AND reading_date = '2026-10-15'")
        _ = cur.fetchall()
    t_indexed = time.perf_counter() - t0
    
    print(f"200 Point-Queries Without Index (Full Table Scan) : {t_unindexed:.4f} s")
    print(f"200 Point-Queries With B-Tree Index (B-Tree Seek)  : {t_indexed:.4f} s")
    print(f"Query Speedup Factor with Composite Index        : {t_unindexed / t_indexed:.2f}x")

def run_task_b4():
    print("=" * 80)
    print("ASSIGNMENT 5 - TASK B4: FINAL DECISION & AI APPLICATIONS")
    print("=" * 80)

    # 1. Complete the Code Required Section
    print("\n--- Complete the Code Expected Execution ---")
    for c in ["Roads are clean and the bus was fast.",
              "Smoke from the factory, air is bad.",
              "The staff were not helpful.",
              "Not bad, service improved."]:
        print(f"{label(c):8} | {c}")

    assert label("Roads are clean and the bus was fast.") == "positive"
    assert label("Smoke from the factory, air is bad.") == "negative"
    assert label("The staff were not helpful.") == "negative"
    assert label("Not bad, service improved.") == "positive"
    print("[PASS] Complete the code output matched expected labels exactly!")

    # 2. Evaluate 50 Citizen Complaints
    evaluate_complaints_sentiment()

    # 3. Demonstrate Extractive Summariser
    print("\n--- Extractive Text Summariser Demonstration ---")
    long_complaint = (
        "Thick black smoke has been billowing from the industrial processing unit since 4 AM. "
        "Residents in nearby residential apartments are experiencing severe coughing and eye irritation. "
        "The municipal grievance helpline was contacted three times but no field officer visited. "
        "Immediate inspection and particulate emission testing must be conducted by the pollution board."
    )
    summary_res = extractive_summarise(long_complaint, top_k_sentences=2)
    print("Original Text Length:", len(long_complaint.split()), "words")
    print("Extractive 2-Sentence Summary:")
    print(f"\"{summary_res}\"")

    # 4. Chatbot and Database Indexing
    if os.path.exists(DB_PATH):
        con = sqlite3.connect(DB_PATH)
        benchmark_database_index(con)

        print("\n--- Conversational Chatbot Interactions ---")
        chat_queries = [
            "What is the PM2.5 in Adyar today?",
            "What is the air quality in Manali?",
            "Which stations are being monitored?",
            "Can you tell me about the weather?"
        ]
        for q in chat_queries:
            reply = chatbot_query(q, con)
            print(f"Citizen : {q}")
            print(f"Chatbot : {reply}\n")
        con.close()

    # 5. Production Decision for 100 Stations at 15-Minute Frequency
    print("--- B4.3: Final Production Engineering Decision ---")
    print("Scale Analysis: 100 stations x 4 readings/hr x 24 hrs x 365 days = ~3.5 Million telemetry records/year.")
    print("1. Telemetry Ingestion: SQLite with composite B-Tree indexes on (station, reading_date) is highly capable of")
    print("   handling 3.5M rows (< 400 MB storage). However, for concurrent multi-station write streaming,")
    print("   PostgreSQL or TimescaleDB time-series database is recommended to avoid SQLite database lock contention.")
    print("2. AI Strategy: The rule-based lexicon achieved ~85-90% accuracy on basic citizen feedback.")
    print("   However, for 50,000 monthly complaints involving complex local Tamil-English colloquialisms and sarcasm,")
    print("   a fine-tuned transformer model (e.g. IndicBERT / RoBERTa) should be deployed for automated triage.")

if __name__ == "__main__":
    run_task_b4()
