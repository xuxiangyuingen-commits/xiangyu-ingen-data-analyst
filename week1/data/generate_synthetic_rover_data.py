import csv
import random
from datetime import datetime, timedelta
from pathlib import Path

# Set random seed so the result is reproducible
random.seed(42)

# Number of rows
n = 15000

# Save CSV in the same folder as this Python file
output_path = Path(__file__).parent / "synthetic_rover_data.csv"

# Start time
start_time = datetime(2026, 6, 22, 0, 0, 0)

# Column names
columns = [
    "timestamp",
    "unit_id",
    "gps_lat",
    "gps_lon",
    "lidar_dist",
    "battery_soc",
    "torque_fl",
    "torque_fr",
    "torque_rl",
    "torque_rr",
    "ambient_temp",
    "fault_label"
]

rows = []

for i in range(n):
    # About 12% fault rate
    fault_label = 1 if random.random() < 0.12 else 0

    timestamp = start_time + timedelta(minutes=i)
    unit_id = f"ROVER_{random.randint(1, 20):02d}"

    # GPS around Santa Clara
    gps_lat = random.gauss(37.3875, 0.01)
    gps_lon = random.gauss(-121.9720, 0.01)

    if fault_label == 1:
        # Fault rows: lower battery, more unstable LiDAR and torque
        battery_soc = random.gauss(38, 12)
        lidar_dist = random.gauss(4.5, 2.0)
        torque_base = random.gauss(18, 6)
    else:
        # Normal rows
        battery_soc = random.gauss(68, 15)
        lidar_dist = random.gauss(3.0, 0.8)
        torque_base = random.gauss(10, 3)

    # Keep values in reasonable ranges
    battery_soc = max(0, min(100, battery_soc))
    lidar_dist = max(0.1, lidar_dist)

    torque_fl = torque_base + random.gauss(0, 1.5)
    torque_fr = torque_base + random.gauss(0, 1.5)
    torque_rl = torque_base + random.gauss(0, 1.5)
    torque_rr = torque_base + random.gauss(0, 1.5)

    ambient_temp = random.gauss(24, 5)

    rows.append([
        timestamp,
        unit_id,
        round(gps_lat, 6),
        round(gps_lon, 6),
        round(lidar_dist, 3),
        round(battery_soc, 2),
        round(torque_fl, 3),
        round(torque_fr, 3),
        round(torque_rl, 3),
        round(torque_rr, 3),
        round(ambient_temp, 2),
        fault_label
    ])

# Write CSV file
with open(output_path, "w", newline="", encoding="utf-8") as file:
    writer = csv.writer(file)
    writer.writerow(columns)
    writer.writerows(rows)

# Print simple summary
fault_count = sum(row[-1] for row in rows)
fault_rate = fault_count / n

print("Synthetic Aido Rover dataset created successfully.")
print("File saved to:", output_path)
print("Rows:", n)
print("Columns:", len(columns))
print("Fault count:", fault_count)
print("Fault rate:", round(fault_rate, 4))
print("First row:")
print(rows[0])