# W02 SQL Analysis Report

## Problem Statement

This report uses a simulated SQLite fleet database to analyze Aido Rover fleet health and Sentinel Prime AI event patterns. The goal is to identify high-risk rover units, deployment zones with elevated fault rates, possible firmware-level reliability patterns, sensor differences between normal and fault operation, and high-risk Sentinel Prime AI security zones.

This analysis supports the broader Week 2 objective of using SQL as a complementary tool to Python-based exploratory data analysis. Instead of only analyzing the synthetic rover dataset in a notebook, SQL allows the data analyst to query structured fleet data directly and answer operational questions that are relevant to robot deployment, maintenance, and platform monitoring.

## Data Source

The SQLite database contains three simulated tables:

* `rover_telemetry`: synthetic Aido Rover telemetry data generated from the Week 1 dataset
* `rover_units`: simulated metadata for 20 Aido Rover units, including deployment zone, firmware version, deployment start date, and operating hours
* `sentinel_events`: simulated Sentinel Prime AI event logs across multiple location zones

All data used in this report is synthetic. It does not contain InGen Dynamics confidential information, customer data, internal systems data, or proprietary documentation.

---

## Key Finding 1: Highest-Fault Rover Units

### Business Question

Which Aido Rover units have the highest observed fault rates?

### SQL Result

The SQL query grouped telemetry records by `unit_id` and calculated the average value of `fault_label` as the observed fault rate for each rover unit.

The highest-fault units were:

| Rover Unit | Average Battery SoC | Fault Rate | Total Records |
| ---------- | ------------------: | ---------: | ------------: |
| ROVER_11   |               64.02 |     13.82% |           767 |
| ROVER_10   |               64.12 |     13.61% |           786 |
| ROVER_09   |               63.66 |     13.43% |           715 |
| ROVER_01   |               63.46 |     13.40% |           754 |
| ROVER_07   |               63.76 |     13.27% |           746 |

ROVER_11 had the highest observed fault rate at approximately 13.82%, followed by ROVER_10 at 13.61% and ROVER_09 at 13.43%.

### Deployment Implication

These rover units should be prioritized for closer monitoring in later fleet health analysis. From an Aido Rover fleet management perspective, high-fault units may need maintenance review, firmware validation, sensor-level inspection, or additional monitoring during future deployments.

This result also shows why SQL is useful in fleet analytics: a simple grouped query can quickly identify which units should receive operational attention before more advanced statistical modeling begins.

---

## Key Finding 2: Fault Rate by Deployment Zone

### Business Question

Which deployment zones are associated with higher Aido Rover fault rates?

### SQL Result

The SQL query joined `rover_telemetry` with `rover_units`, grouped records by `deployment_zone`, and calculated average battery state of charge and observed fault rate.

| Deployment Zone | Average Battery SoC | Fault Rate | Total Records |
| --------------- | ------------------: | ---------: | ------------: |
| Zone D          |               63.93 |     13.55% |         1,513 |
| Zone A          |               64.26 |     12.43% |         4,498 |
| Zone C          |               64.47 |     12.32% |         4,547 |
| Zone B          |               64.40 |     12.11% |         4,442 |

Zone D had the highest observed fault rate at approximately 13.55%. Zone B had the lowest observed fault rate at approximately 12.11%.

### Deployment Implication

Zone D may have operating conditions associated with higher rover fault risk. Possible explanations could include terrain difficulty, navigation complexity, environmental conditions, patrol route structure, or uneven deployment load. Because this is a synthetic dataset, this result should not be interpreted as a real operational issue. However, in a real fleet setting, this type of SQL query would help identify whether location context is related to robot reliability.

For future analysis, deployment zone should be considered as a contextual variable when studying Aido Rover fault probability.

---

## Key Finding 3: Fault Rate by Firmware Version

### Business Question

Does Aido Rover fault rate differ by firmware version?

### SQL Result

The SQL query joined `rover_telemetry` with `rover_units`, grouped records by `firmware_version`, and calculated the observed fault rate for each version.

| Firmware Version | Fault Rate | Average Battery SoC | Total Records |
| ---------------- | ---------: | ------------------: | ------------: |
| v1.2             |     13.09% |               64.06 |         4,499 |
| v1.1             |     12.37% |               64.36 |         3,782 |
| v1.0             |     12.06% |               64.38 |         4,452 |
| v2.0             |     11.82% |               64.70 |         2,267 |

Firmware version v1.2 had the highest observed fault rate at approximately 13.09%, while v2.0 had the lowest observed fault rate at approximately 11.82%.

### Deployment Implication

In this simulated dataset, firmware version appears to be worth tracking as a fleet reliability variable. If this pattern appeared in real operational data, it could suggest that one firmware version may require additional testing, rollback review, or performance comparison against newer versions.

However, this finding should be interpreted carefully. SQL shows an association, not causation. A higher fault rate for one firmware version may be related to other factors such as deployment zone, unit age, operating hours, or route difficulty. A later regression model could help test whether firmware version still matters after controlling for other variables.

---

## Key Finding 4: Sensor Differences Between Normal and Fault Rows

### Business Question

Which sensor variables show the largest differences between normal operation and fault operation?

### SQL Result

The SQL query grouped records by `fault_label` and compared average battery state of charge, LiDAR distance, and four wheel torque values.

| Fault Label | Avg Battery SoC | Avg LiDAR Distance | Avg Torque FL | Avg Torque FR | Avg Torque RL | Avg Torque RR | Total Records |
| ----------- | --------------: | -----------------: | ------------: | ------------: | ------------: | ------------: | ------------: |
| 0 = Normal  |           68.00 |               2.99 |          9.97 |          9.97 |          9.66 |          9.52 |        13,138 |
| 1 = Fault   |           38.45 |               4.56 |         17.91 |         17.99 |         17.94 |         17.92 |         1,862 |

The largest difference appears in battery state of charge. Normal rows had an average battery state of charge of approximately 68.00, while fault rows had an average battery state of charge of approximately 38.45.

Fault rows also had higher average LiDAR distance values. Normal rows had an average LiDAR distance of approximately 2.99, while fault rows had an average LiDAR distance of approximately 4.56.

The four wheel torque values were also much higher in fault rows. Normal rows had average wheel torque values around 9.5 to 10.0, while fault rows had average wheel torque values around 17.9.

### Deployment Implication

Battery state of charge, LiDAR distance, and wheel torque appear to be useful candidate predictors for later correlation analysis, regression modeling, and predictive fault classification.

From a fleet management perspective, these variables may act as early warning indicators. Low battery state of charge may reflect power-related risk, higher LiDAR distance may indicate more difficult navigation conditions or sensor instability, and higher wheel torque may suggest increased mechanical load or movement difficulty.

This finding directly supports the Week 3 regression task. These variables should be tested as candidate predictors when modeling Aido Rover fault status.

---

## Key Finding 5: Sentinel Severity-3 Events by Zone

### Business Question

Which Sentinel Prime AI location zone has the highest number of severity-3 events?

### SQL Result

The SQL query filtered `sentinel_events` to severity-3 events, grouped them by `location_zone`, and counted the number of high-severity events in each zone.

| Location Zone | Severity-3 Events |
| ------------- | ----------------: |
| Zone C        |                38 |
| Zone A        |                37 |
| Zone D        |                34 |
| Zone B        |                32 |

Zone C had the highest number of severity-3 events, with 38 events. Zone A followed closely with 37 events, while Zone D had 34 and Zone B had 32.

### Deployment Implication

Zone C and Zone A may require closer monitoring in the Sentinel Prime AI context. If this were real operational data, these zones could be candidates for additional sensor coverage, event review, patrol adjustment, or security resource allocation.

This finding also shows how SQL can be used beyond Aido Rover telemetry. The same database approach can support security event analysis for Sentinel Prime AI by summarizing event frequency, severity level, location zone, and event type.

---

## Recommendation

Based on the SQL findings, the next stage of analysis should prioritize three directions.

First, Aido Rover fleet monitoring should pay closer attention to high-fault units such as ROVER_11, ROVER_10, and ROVER_09. These units may be useful cases for later fault pattern investigation.

Second, deployment zone and firmware version should be included as contextual variables in future analysis. Zone D showed the highest observed fault rate, and firmware version v1.2 showed the highest observed fault rate among firmware groups. These results do not prove causation, but they suggest useful directions for deeper analysis.

Third, battery state of charge, LiDAR distance, and wheel torque should be used as candidate predictors in Week 3 correlation analysis and multivariate regression. The SQL comparison between normal and fault rows shows clear differences in these sensor variables, making them strong starting points for statistical modeling.

Overall, the Week 2 SQL analysis demonstrates that structured queries can quickly identify fleet-level patterns, high-risk units, sensor differences, and event concentrations. These findings prepare the project for Week 3, where correlation analysis and regression modeling will test which variables are the strongest determinants of Aido Rover fault status.
