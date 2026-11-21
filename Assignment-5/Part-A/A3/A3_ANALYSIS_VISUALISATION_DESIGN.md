# TASK A3: DESIGN THE ANALYSIS AND VISUALISATION

---

### A3.1: Selection and Justification of Chart Types

1. **Monthly Trend of PM2.5**:
   - *Chart Choice*: **Continuous Line Plot** (`matplotlib.pyplot.plot`).
   - *Justification*: Time is a continuous, ordered dimension. A line plot highlights temporal progressions, identifying weekend dips, weekly commuting surges, and progressive seasonal deterioration.
2. **Comparison of Stations**:
   - *Chart Choice*: **Categorical Bar Chart** (`matplotlib.pyplot.bar`).
   - *Justification*: The 12 monitoring stations represent discrete, unordered nominal spatial categories. A horizontal or vertical bar chart with sorted values allows citizens and policymakers to immediately rank stations from cleanest to most polluted.
3. **Relationship between Temperature and PM2.5**:
   - *Chart Choice*: **Bivariate Scatter Plot with Trend Line** (`matplotlib.pyplot.scatter`).
   - *Justification*: Evaluates physical atmospheric correlation. Scatter plots expose non-linear relationships, such as thermal inversion trapping particulates during low-temperature morning hours.
4. **Hours with the Worst Air Quality**:
   - *Chart Choice*: **Hourly Distribution Box Plot or Grouped Bar Chart** (`matplotlib.pyplot.boxplot` or `bar`).
   - *Justification*: Across 24 hours of the diurnal cycle, pollution peaks during peak vehicular traffic (08:00–10:00 and 18:00–21:00). A box plot visualizes the median, interquartile range (IQR), and extreme spikes per hour.

---

### A3.2: Daily Summary Table Design
The board requires a daily summary view per station:

| Station Name | Date | Min PM2.5 | Max PM2.5 | Mean PM2.5 | Valid Readings Count | Air Quality Status |
|---|---|---|---|---|---|---|
| Adyar | 2026-10-01 | 18.0 | 72.0 | 45.30 | 24 | Moderate |
| Guindy | 2026-10-01 | 35.0 | 185.0 | 98.40 | 23 | Poor |

#### Production Method:
Using an optimized SQL query:
```sql
SELECT
    station_name,
    reading_date,
    MIN(pm25) AS min_pm25,
    MAX(pm25) AS max_pm25,
    ROUND(AVG(pm25), 2) AS mean_pm25,
    COUNT(pm25) AS valid_readings_count,
    CASE
        WHEN AVG(pm25) <= 30 THEN 'Good'
        WHEN AVG(pm25) <= 60 THEN 'Satisfactory'
        WHEN AVG(pm25) <= 90 THEN 'Moderate'
        WHEN AVG(pm25) <= 120 THEN 'Poor'
        ELSE 'Very Poor'
    END AS aqi_status
FROM readings
GROUP BY station_name, reading_date;
```
