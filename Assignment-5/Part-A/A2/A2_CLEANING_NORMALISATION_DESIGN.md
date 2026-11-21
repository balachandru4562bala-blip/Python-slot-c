# TASK A2: DESIGN THE CLEANING AND NORMALISATION

---

### A2.1: Data Cleaning Rules Specification

1. **Missing or Blank Values**:
   - *Rule*: For air quality reporting, if an hourly pollutant value is blank or `'NA'`, forward-fill ($LOCF$) from the immediate previous hour if the gap is $\le 2$ consecutive hours. If gap $> 2$ hours, drop the reading from daily hourly summaries to prevent synthetic bias.
   - *Justification*: Atmospheric air quality exhibits strong auto-correlation over 1-2 hour windows. Imputing median over long gaps obscures micro-climate pollution spikes.
2. **Impossible / Corrupt Values**:
   - *Rule*: Discard any PM2.5 $< 0.0$ or $> 999.0\ \mu\text{g/m}^3$. Discard PM10 $< 0.0$ or $> 1500.0\ \mu\text{g/m}^3$.
   - *Justification*: Negative values are optical calibration drift; values above $999$ indicate sensor saturation/electrical shorts.
3. **Duplicate Rows**:
   - *Rule*: Enforce uniqueness constraint on `(station_name, reading_date, reading_hour)`. If duplicate received, retain the latest non-null reading.
   - *Justification*: Retransmission retry bursts should not artificially double pollution weighting.
4. **Fahrenheit to Celsius Normalisation**:
   - *Rule*: Detect if station is tagged as Fahrenheit (or if temperature $> 60.0^\circ$ and station is known legacy), apply standard formula:
     $$C = \frac{F - 32}{1.8}$$
   - *Justification*: Ambient air in Chennai fluctuates between $20^\circ\text{C}$ and $42^\circ\text{C}$. A reading of $86^\circ$ is $30^\circ\text{C}$.

---

### A2.2: Feature Normalisation and Scaling
To feed downstream machine learning and multi-station comparative dashboards, two scaling designs are formulated:

1. **Min-Max Normalisation (Range [0, 1])**:
   $$x_{\text{scaled}} = \frac{x - x_{\min}}{x_{\max} - x_{\min}}$$
   - *Use Case*: Air Quality Index (AQI) gauge visualization and normalized comparative trend plotting where bounded $[0, 1]$ intervals are required.
2. **Z-Score Standardisation ($\mu = 0, \sigma = 1$)**:
   $$z = \frac{x - \mu}{\sigma}$$
   - *Use Case*: Statistical anomaly and spike detection. Readings with $|z| > 3.0$ are immediately flagged as statistical outliers or localized industrial pollution incidents.

---

### A2.3: Standard Formats Specification
- **Dates**: Strict ISO-8601 standard: `YYYY-MM-DD` (e.g., `2026-10-01`).
- **Station Names**: Canonical Title Case without leading/trailing whitespace (e.g., `"  adyar "` -> `"Adyar"`).
- **Numeric Precision**: Floating-point formatted to exactly 2 decimal places for pollutants (e.g., `48.25`) and 1 decimal place for ambient temperature (`29.4`).
