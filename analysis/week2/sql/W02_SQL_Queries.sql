-- W02 SQL Queries
-- Data Analyst Internship Program
-- Xiangyu Xu
-- Database: fleet.db


-- Query 1
-- Business question:
-- What is the average battery state of charge and fault rate for the entire Aido Rover fleet?
-- Platform implication:
-- This gives a high-level fleet health baseline for Aido Rover operations.

    SELECT
        AVG(battery_soc) AS avg_battery_soc,
        AVG(fault_label) AS fleet_fault_rate,
        COUNT(*) AS total_records
    FROM rover_telemetry;


-- Query 2
-- Business question:
-- What is the average battery state of charge and fault rate by rover unit?
-- Platform implication:
-- This helps identify individual Aido Rover units with weaker operational health.

SELECT
    unit_id,
    AVG(battery_soc) AS avg_battery_soc,
    AVG(fault_label) AS fault_rate,
    COUNT(*) AS total_records
FROM rover_telemetry
GROUP BY unit_id
ORDER BY fault_rate DESC;


-- Query 3
-- Business question:
-- Which rover units have a fault rate above 15%?
-- Platform implication:
-- These units should be prioritized for maintenance review or closer monitoring.

SELECT
    unit_id,
    AVG(fault_label) AS fault_rate,
    COUNT(*) AS total_records
FROM rover_telemetry
GROUP BY unit_id
HAVING AVG(fault_label) > 0.15
ORDER BY fault_rate DESC;


-- Query 4
-- Business question:
-- What is the average battery state of charge and fault rate by deployment zone?
-- Platform implication:
-- This helps determine whether certain deployment zones are associated with higher fault risk.

SELECT
    u.deployment_zone,
    AVG(t.battery_soc) AS avg_battery_soc,
    AVG(t.fault_label) AS fault_rate,
    COUNT(*) AS total_records
FROM rover_telemetry t
JOIN rover_units u
    ON t.unit_id = u.unit_id
GROUP BY u.deployment_zone
ORDER BY fault_rate DESC;


-- Query 5
-- Business question:
-- Does fault rate differ by firmware version?
-- Platform implication:
-- This helps determine whether firmware version may be related to Aido Rover reliability.

SELECT
    u.firmware_version,
    AVG(t.fault_label) AS fault_rate,
    AVG(t.battery_soc) AS avg_battery_soc,
    COUNT(*) AS total_records
FROM rover_telemetry t
JOIN rover_units u
    ON t.unit_id = u.unit_id
GROUP BY u.firmware_version
ORDER BY fault_rate DESC;


-- Query 6
-- Business question:
-- Which five rover units have the highest fault rates?
-- Platform implication:
-- These units may require priority inspection before broader fleet deployment.

WITH unit_faults AS (
    SELECT
        unit_id,
        AVG(fault_label) AS fault_rate,
        COUNT(*) AS total_records
    FROM rover_telemetry
    GROUP BY unit_id
)
SELECT
    unit_id,
    fault_rate,
    total_records
FROM unit_faults
ORDER BY fault_rate DESC
LIMIT 5;


-- Query 7
-- Business question:
-- What is the average LiDAR distance and wheel torque for normal vs. fault rows?
-- Platform implication:
-- This helps identify sensor patterns that may separate normal operation from fault operation.

SELECT
    fault_label,
    AVG(battery_soc) AS avg_battery_soc,
    AVG(lidar_dist) AS avg_lidar_dist,
    AVG(torque_fl) AS avg_torque_fl,
    AVG(torque_fr) AS avg_torque_fr,
    AVG(torque_rl) AS avg_torque_rl,
    AVG(torque_rr) AS avg_torque_rr,
    COUNT(*) AS total_records
FROM rover_telemetry
GROUP BY fault_label;


-- Query 8
-- Business question:
-- Which deployment zone has the lowest average battery state of charge?
-- Platform implication:
-- Low battery levels by zone may indicate higher operational load or charging issues.

SELECT
    u.deployment_zone,
    AVG(t.battery_soc) AS avg_battery_soc,
    COUNT(*) AS total_records
FROM rover_telemetry t
JOIN rover_units u
    ON t.unit_id = u.unit_id
GROUP BY u.deployment_zone
ORDER BY avg_battery_soc ASC;


-- Query 9
-- Business question:
-- What is the 7-record rolling average battery state of charge for each rover unit?
-- Platform implication:
-- Rolling averages help detect declining battery trends before they become operational faults.

SELECT
    unit_id,
    timestamp,
    battery_soc,
    AVG(battery_soc) OVER (
        PARTITION BY unit_id
        ORDER BY timestamp
        ROWS BETWEEN 6 PRECEDING AND CURRENT ROW
    ) AS rolling_avg_battery_soc
FROM rover_telemetry
ORDER BY unit_id, timestamp
LIMIT 100;


-- Query 10
-- Business question:
-- Which Sentinel Prime AI location zone has the most severity-3 events?
-- Platform implication:
-- This helps identify security zones that may require stronger monitoring or resource allocation.

SELECT
    location_zone,
    COUNT(*) AS severity_3_events
FROM sentinel_events
WHERE severity = 3
GROUP BY location_zone
ORDER BY severity_3_events DESC;


-- Query 11
-- Business question:
-- What are the most common Sentinel Prime AI event types?
-- Platform implication:
-- This helps understand which types of security events occur most often across monitored zones.

SELECT
    event_type,
    COUNT(*) AS event_count
FROM sentinel_events
GROUP BY event_type
ORDER BY event_count DESC;


-- Query 12
-- Business question:
-- What is the average severity of Sentinel events by location zone?
-- Platform implication:
-- This helps compare risk levels across different Sentinel Prime AI deployment zones.

SELECT
    location_zone,
    AVG(severity) AS avg_severity,
    COUNT(*) AS total_events
FROM sentinel_events
GROUP BY location_zone
ORDER BY avg_severity DESC;