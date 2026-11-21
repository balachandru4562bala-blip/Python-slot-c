# Assignment 5: Data Analysis, Visualisation and AI Applications

**Course Outcome**: CO5 — Develop Python programs using libraries and tools to acquire, clean, visualise, and analyse data from CSV files and SQL databases  
**Bloom's Levels**: K3 Apply, K4 Analyse, K5 Evaluate  
**Total Marks**: 50 (Part A: 25 Marks, Part B: 25 Marks)  
**Case Study**: City Air-Quality Monitoring Network (12 Urban Stations & Citizen Grievance Analytics)  

---

## 1. Assignment Objectives
- Formulate end-to-end data acquisition and relational schema designs in SQLite with composite indexing.
- Implement robust telemetry cleaning rules: forward-filling missing values, dropping non-physical sensor spikes ($> 999\ \mu\text{g/m}^3$), negative calibration drift, and converting Fahrenheit to Celsius.
- Compute feature scaling using Min-Max Normalisation ($[0, 1]$) and Z-Score Standardisation.
- Render high-resolution publication-quality visualisations using Matplotlib across four analytical dimensions.
- Perform empirical benchmark comparisons among Plain Python loops, Pandas vectorised operations, and SQLite `GROUP BY` queries.
- Profile runtime bottlenecks using `cProfile` and deterministic execution statistics.
- Build introductory AI applications: a negation-aware lexicon sentiment scorer, an extractive text summariser, and a rule-based conversational chatbot querying live SQL databases.

---

## 2. Directory Structure

```
Assignment-5/
├── Part-A/
│   ├── A1/
│   │   └── A1_DATA_ACQUISITION_DESIGN.md       # Source analysis, SQLite schema, CSV vs SQL comparison
│   ├── A2/
│   │   └── A2_CLEANING_NORMALISATION_DESIGN.md # Imputation rules, min-max & z-score, standardization
│   ├── A3/
│   │   └── A3_ANALYSIS_VISUALISATION_DESIGN.md # Chart selection rationales and summary table design
│   ├── A4/
│   │   └── A4_DEBUGGING_PROFILING_PLAN.md      # Debugging (logging/pdb) and profiling (cProfile/timeit)
│   └── A5/
│   │   └── A5_AI_APPLICATION_DESIGN.md        # Sentiment algorithm, summarizer, rule-based chatbot
│
├── Part-B/
│   ├── B1/
│   │   └── cleaning_pipeline.py                # Complete the Code TODO 1 & 2, SQLite loader, chart generator
│   ├── B2/
│   │   └── adversarial_testing.py              # Complete the Code TODO 1 & 2, SQL injection & robustness
│   ├── B3/
│   │   └── loops_vs_pandas_vs_sql.py           # Multi-scale benchmark (8.7k to 260k rows) & cProfile
│   └── B4/
│       └── final_decision_ai.py                # Complete the Code TODO 1, 50 complaints test, chatbot, scaling
│
├── data/                                       # Telemetry and complaints raw data staging
├── database/
│   └── air_quality.db                          # Cleaned SQLite persistent database with composite indexes
├── charts/
│   ├── chart1_pm25_monthly_trend.png           # Line plot: Daily mean PM2.5 trend
│   ├── chart2_station_comparison.png           # Horizontal bar chart: Station comparison
│   ├── chart3_temp_vs_pm25_scatter.png         # Scatter plot: Temperature vs PM2.5 correlation
│   └── chart4_hourly_worst_air.png             # Bar chart: City-wide diurnal hourly pollution profile
├── test_results.txt                            # Verified test execution log
├── requirements.txt                            # Python dependencies (pandas, matplotlib)
└── README.md                                   # Comprehensive assignment documentation
```

---

## 3. Description of Tasks and Implementations

### Part A: Data and Program Design (Specifications & Pseudocode)
- **A1**: Formulates CSV inspection, data quality failure taxonomy, and normalized relational SQLite schema. Proves SQL indexed lookup is $\approx 100\times$ faster than repeated CSV file scans.
- **A2**: Defines mathematical cleaning rules: forward-fill interpolation for $\le 2$-hour sensor gaps, dropping negative values and $> 999\ \mu\text{g/m}^3$ outliers, Fahrenheit-to-Celsius conversion, and min-max/z-score scaling.
- **A3**: Justifies line charts for time-series trends, bar charts for station comparisons, scatter plots for physical correlations, and hourly bar charts for diurnal rush-hour tracking.
- **A4**: Outlines production debugging strategy (logging hierarchy vs print) and CPU deterministic profiling (`cProfile`, `time.perf_counter`).
- **A5**: Specifies a negation-handling sentiment lexicon, word-frequency extractive summariser, and conversational chatbot architecture.

### Part B: Implementation and Experimental Investigation
- **B1**: Completes TODO 1 (`load_clean`) and TODO 2 (`min_max`). Adds outlier filter ($> 999$). Builds SQLite database (`database/air_quality.db`) with `executemany`. Generates all 4 Matplotlib figures in `charts/` with technical interpretations.
- **B2**: Completes TODO 1 and TODO 2 with parameterised `?` queries. Demonstrates SQL injection security: parameterised queries treat `'Adyar\' OR \'1\'=\'1'` as a literal text string, preventing unauthorized data dumping. Tests adversarial files and sentiment sarcasm.
- **B3**: Computes daily mean PM2.5 across Plain Python loops, Pandas `groupby`, and SQLite `GROUP BY`. Proves all three agree. Evaluates multi-scale dataset sizes up to 259,200 rows. Profiles Python loop using `cProfile`.
- **B4**: Completes TODO 1 in `score(text)`. Evaluates sentiment classifier across 50 real citizen complaints (achieving $\ge 88\%$ human agreement). Demonstrates 2-sentence extractive text summariser. Evaluates $3\times$ database query speedup with composite B-Tree index. Runs conversational chatbot querying live SQL.

---

## 4. Execution Commands

Ensure requirements are installed:
```bash
pip install -r Assignment-5/requirements.txt
```

Run Part B programs:
```bash
# B1: Cleaning Pipeline, SQLite DB Population, and Chart Generation
python Assignment-5/Part-B/B1/cleaning_pipeline.py

# B2: Adversarial Testing and SQL Injection Defense
python Assignment-5/Part-B/B2/adversarial_testing.py

# B3: Loops vs Pandas vs SQL Scaling Benchmark & cProfile
python Assignment-5/Part-B/B3/loops_vs_pandas_vs_sql.py

# B4: Final Decision, 50 Complaints Test, Summariser, and Chatbot
python Assignment-5/Part-B/B4/final_decision_ai.py
```
