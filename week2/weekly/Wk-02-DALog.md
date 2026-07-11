# Week 2 Data Analyst Log

## What I Analyzed

This week, I converted the synthetic Aido Rover telemetry dataset from Week 1 into a simulated SQLite fleet database. The database includes three tables: `rover_telemetry`, `rover_units`, and `sentinel_events`. I used SQL queries to analyze rover unit fault rates, deployment zone patterns, firmware version differences, sensor differences between normal and fault rows, and Sentinel Prime AI severity-3 event patterns.

## What I Found

The most important SQL finding was that fault rows showed clear sensor differences compared with normal rows. Fault rows had much lower average battery state of charge, higher average LiDAR distance, and much higher wheel torque values across all four wheels. This suggests that battery level, LiDAR distance, and wheel torque may be useful candidate predictors for later correlation analysis and regression modeling.

## Most Surprising SQL Finding

The most surprising finding was that the deployment zone and firmware version also showed different observed fault rates. Zone D had the highest observed fault rate at approximately 13.55%, while firmware version v1.2 had the highest observed fault rate at approximately 13.09%. Although this is synthetic data and does not prove causation, it shows how SQL can help identify operational patterns before statistical modeling begins.

## Operational Implication

For Aido Rover fleet management, SQL can quickly identify high-risk units, higher-risk zones, and possible firmware-level reliability patterns. This type of analysis would help a fleet manager decide which units or deployment contexts should be reviewed first.

## Next Step

The Week 2 SQL findings will support Week 3 correlation analysis and multivariate regression. Battery state of charge, LiDAR distance, and wheel torque will be treated as candidate predictors for Aido Rover fault status.