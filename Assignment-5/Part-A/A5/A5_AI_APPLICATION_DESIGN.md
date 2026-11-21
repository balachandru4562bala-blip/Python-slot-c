# TASK A5: DESIGN AN INTRODUCTORY AI APPLICATION FOR CITIZEN COMPLAINTS

---

### A5.1: Lexicon Sentiment Scorer and Extractive Summariser

#### 1. Negation-Aware Lexicon Sentiment Scorer
- **Lexicon Dictionaries**:
  - `POSITIVE_WORDS = {"clean", "good", "fast", "helpful", "improved", "fresh", "prompt", "resolved"}`
  - `NEGATIVE_WORDS = {"bad", "dirty", "smoke", "polluted", "slow", "rude", "cough", "burning", "garbage", "smell"}`
  - `NEGATION_WORDS = {"not", "never", "no", "hardly", "barely"}`
- **Algorithm**:
  - Tokenize text into words, stripping punctuation.
  - Maintain a running sentiment score initialized to 0.
  - Iterate through tokens:
    - If token in `POSITIVE_WORDS`, assign $+1$.
    - If token in `NEGATIVE_WORDS`, assign $-1$.
    - Check preceding token: If `tokens[i-1]` in `NEGATION_WORDS`, flip sign (e.g. "not good" becomes $-1$, "not bad" becomes $+1$).
    - Add to total sentiment score.
  - Classification: `score > 0 -> "Positive"`, `score < 0 -> "Negative"`, `score == 0 -> "Neutral"`.

#### 2. Frequency-Based Extractive Text Summariser
- **Algorithm**:
  - Segment document text into sentences.
  - Tokenize and compute word frequency distribution, excluding common stopwords (`is`, `the`, `and`, `of`, `to`, `in`).
  - Score each sentence by summing the normalized frequency weights of its constituent non-stop words.
  - Select the top $k$ highest-scoring sentences (default $k = 2$) in their original chronological sequence to form a coherent extractive summary.

---

### A5.2: Rule-Based Conversational Chatbot
- **Intent Pattern Matching**:
  - Intent 1: Current pollution check (`"what is the pm25 in <station>"`, `"air quality in <station>"`).
    - Extracted Entity: `station_name`.
    - Backend Action: `SELECT pm25, temperature_c FROM readings WHERE station_name = ? ORDER BY reading_date DESC, reading_hour DESC LIMIT 1`.
  - Intent 2: Daily safety advice (`"is it safe to walk in <station>"`, `"health advisory"`).
    - Backend Action: Query average PM2.5; evaluate threshold:
      - $\le 60\ \mu\text{g/m}^3$: "Air quality is good/satisfactory. Safe for outdoor activities."
      - $> 60\ \mu\text{g/m}^3$: "Air quality is poor. Elderly individuals and children should wear N95 masks."
  - Intent 3: Station list inquiry (`"which stations are monitored"`, `"show stations"`).
    - Backend Action: `SELECT DISTINCT station_name FROM readings`.
- **Known Limitations of Rule-Based Chatbot**:
  1. Cannot resolve typos or phonetic spelling errors (e.g. "Adiyaru" instead of "Adyar").
  2. Lacks semantic contextual understanding and dialogue history (stateless).
  3. Fails on complex compound requests (e.g., "Compare Adyar and Guindy air quality yesterday evening").
