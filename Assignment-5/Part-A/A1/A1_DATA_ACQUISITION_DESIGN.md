# TASK A1: DESIGN THE DATA ACQUISITION
## City Air-Quality Monitoring Network

---

### A1.1: Inspect the Source and Identify Data-Quality Problems
The 12 city monitoring stations generate hourly CSV telemetry records with the following schema:
`station,date,hour,pm25,pm10,no2,temperature`

#### Anticipated Data-Quality Problems:
1. **Missing or Blank Values**: Sensors momentarily drop telemetry frames due to GSM drops (`Adyar,2026-10-01,14,,45.0,22.1,28.5`).
2. **"NA" / Sentinels as Strings**: Instrument firmware outputs `"NA"`, `"NULL"`, or `"-999"` when laser particle counters reboot (`Guindy,2026-10-01,15,NA,50.0,24.0,29.0`).
3. **Negative Readings**: Zero-point calibration drift in optical scattering chambers produces non-physical negative pollutant densities (`Royapuram,2026-10-01,02,-12.0,30.0,18.0,26.5`).
4. **Extreme Spikes / Outliers**: Sensor hardware voltage surges report impossibly large numbers (`Velachery,2026-10-01,18,9999.0,85.0,34.0,30.0`). Valid PM2.5 in Chennai rarely exceeds $500\ \mu\text{g/m}^3$; readings $> 999\ \mu\text{g/m}^3$ indicate physical fault.
5. **Inconsistent Temperature Units**: Two legacy stations (e.g., Alandur and T. Nagar) report ambient temperature in Fahrenheit ($86.0^\circ\text{F}$) while all other 10 stations report in Celsius ($30.0^\circ\text{C}$).
6. **Duplicate Transmissions**: Network retries deliver identical timestamped records twice.

---

### A1.2: SQLite Relational Database Design
To guarantee relational integrity, fast indexed filtering, and historical durability, a normalized 2-table schema is established:

```sql
-- Stations Metadata Table
CREATE TABLE stations (
    station_id INTEGER PRIMARY KEY AUTOINCREMENT,
    station_name TEXT UNIQUE NOT NULL,
    zone TEXT NOT NULL,
    latitude REAL,
    longitude REAL,
    temp_unit TEXT DEFAULT 'C' -- 'C' or 'F'
);

-- Hourly Cleaned Telemetry Table
CREATE TABLE readings (
    reading_id INTEGER PRIMARY KEY AUTOINCREMENT,
    station_name TEXT NOT NULL,
    reading_date TEXT NOT NULL, -- ISO-8601 YYYY-MM-DD
    reading_hour INTEGER NOT NULL CHECK(reading_hour BETWEEN 0 AND 23),
    pm25 REAL CHECK(pm25 >= 0.0 AND pm25 <= 999.0),
    pm10 REAL CHECK(pm10 >= 0.0 AND pm10 <= 1500.0),
    no2 REAL CHECK(no2 >= 0.0 AND no2 <= 500.0),
    temperature_c REAL CHECK(temperature_c BETWEEN -10.0 AND 60.0),
    FOREIGN KEY (station_name) REFERENCES stations(station_name),
    UNIQUE(station_name, reading_date, reading_hour)
);

-- Performance Index for Rapid Temporal and Spatial Filtering
CREATE INDEX idx_station_date ON readings(station_name, reading_date);
CREATE INDEX idx_date ON readings(reading_date);
```

#### Mapping from CSV Columns to SQL Columns:
- `station` -> `readings.station_name` (Sanitized to Title Case)
- `date` -> `readings.reading_date` (Normalized to `YYYY-MM-DD`)
- `hour` -> `readings.reading_hour` (`int`, 0 to 23)
- `pm25`, `pm10`, `no2` -> `REAL` (Cleaned floats)
- `temperature` -> `temperature_c` (Converted to Celsius if source station reports in Fahrenheit)

---

### A1.3: CSV vs SQL: Query Answering Comparison

| Question of the Board | Answering via Raw CSV Files | Answering via SQLite Database | Verdict |
|---|---|---|---|
| **1. Average PM2.5 in Adyar during October** | Must open all 31 daily CSV files, parse every line, filter for "Adyar" and month 10, accumulate sum and count in Python. Scan Time: $O(N)$ full disk scan. | `SELECT AVG(pm25) FROM readings WHERE station_name = 'Adyar' AND reading_date LIKE '2026-10-%';` Uses index `idx_station_date`, scans only target B-Tree leaves in $< 2$ ms. | **SQL is $100\times$ faster** |
| **2. Peak Monthly Pollution Across All Stations** | Must maintain max variable while scanning all lines in memory. | `SELECT station_name, reading_date, MAX(pm25) FROM readings;` Returns instantly. | **SQL eliminates code complexity** |
| **3. Ranking of Stations by Monthly NO2** | Must aggregate sums and counts in nested Python dictionaries, compute means, and sort via `sorted()`. | `SELECT station_name, AVG(no2) AS mean_no2 FROM readings GROUP BY station_name ORDER BY mean_no2 DESC;` Direct query. | **SQL is declarative and optimized** |

---

### A1.4: Alternative Concept and Complexity Analysis
- **CSV + Pandas**: Loading 105,120 annual records directly from CSV into a DataFrame consumes ~40 MB RAM per query session and requires $O(N)$ sequential parsing every time an analytical script launches.
- **SQLite Database**: Persistent B-Tree storage on disk; indexed queries execute in $O(\log N)$ time, loading only relevant row subsets into RAM ($< 1$ MB).
