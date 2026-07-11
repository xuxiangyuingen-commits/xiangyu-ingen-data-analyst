import csv
import sqlite3
import random
from pathlib import Path
from datetime import datetime, timedelta

random.seed(42)

# Paths
base_dir = Path(__file__).resolve().parent
week1_data_path = base_dir.parent / "week1" / "data" / "synthetic_rover_data.csv"
week2_data_dir = base_dir / "data"
db_path = week2_data_dir / "fleet.db"

week2_data_dir.mkdir(exist_ok=True)

print("Looking for CSV at:", week1_data_path)

if not week1_data_path.exists():
    raise FileNotFoundError(
        "Could not find synthetic_rover_data.csv. "
        "Please check that it is located at analysis/week1/data/synthetic rover data.csv"
    )

# Connect to SQLite database
conn = sqlite3.connect(db_path)
cursor = conn.cursor()

# Drop old tables if they already exist
cursor.execute("DROP TABLE IF EXISTS rover_telemetry")
cursor.execute("DROP TABLE IF EXISTS rover_units")
cursor.execute("DROP TABLE IF EXISTS sentinel_events")

# Create rover_telemetry table
cursor.execute("""
CREATE TABLE rover_telemetry (
    timestamp TEXT,
    unit_id TEXT,
    gps_lat REAL,
    gps_lon REAL,
    lidar_dist REAL,
    battery_soc REAL,
    torque_fl REAL,
    torque_fr REAL,
    torque_rl REAL,
    torque_rr REAL,
    ambient_temp REAL,
    fault_label INTEGER
)
""")

# Load CSV into rover_telemetry
with open(week1_data_path, "r", encoding="utf-8") as file:
    reader = csv.DictReader(file)

    rows = []
    for row in reader:
        rows.append((
            row["timestamp"],
            row["unit_id"],
            float(row["gps_lat"]),
            float(row["gps_lon"]),
            float(row["lidar_dist"]),
            float(row["battery_soc"]),
            float(row["torque_fl"]),
            float(row["torque_fr"]),
            float(row["torque_rl"]),
            float(row["torque_rr"]),
            float(row["ambient_temp"]),
            int(row["fault_label"])
        ))

cursor.executemany("""
INSERT INTO rover_telemetry VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?)
""", rows)

# Create rover_units table
cursor.execute("""
CREATE TABLE rover_units (
    unit_id TEXT PRIMARY KEY,
    deployment_zone TEXT,
    deployment_start_date TEXT,
    firmware_version TEXT,
    total_operating_hours INTEGER
)
""")

zones = ["Zone A", "Zone B", "Zone C", "Zone D"]
firmware_versions = ["v1.0", "v1.1", "v1.2", "v2.0"]

unit_rows = []

for i in range(1, 21):
    unit_id = f"ROVER_{i:02d}"
    deployment_zone = random.choice(zones)
    deployment_start_date = datetime(2026, random.randint(1, 5), random.randint(1, 28)).strftime("%Y-%m-%d")
    firmware_version = random.choice(firmware_versions)
    total_operating_hours = random.randint(200, 1200)

    unit_rows.append((
        unit_id,
        deployment_zone,
        deployment_start_date,
        firmware_version,
        total_operating_hours
    ))

cursor.executemany("""
INSERT INTO rover_units VALUES (?, ?, ?, ?, ?)
""", unit_rows)

# Create sentinel_events table
cursor.execute("""
CREATE TABLE sentinel_events (
    event_id INTEGER PRIMARY KEY,
    timestamp TEXT,
    location_zone TEXT,
    event_type TEXT,
    severity INTEGER
)
""")

event_types = [
    "motion_detected",
    "restricted_area",
    "unknown_object",
    "loitering",
    "system_alert"
]

sentinel_rows = []
start_time = datetime(2026, 6, 22)

for event_id in range(1, 801):
    event_time = start_time + timedelta(
        days=random.randint(0, 30),
        hours=random.randint(0, 23),
        minutes=random.randint(0, 59)
    )

    location_zone = random.choice(zones)
    event_type = random.choice(event_types)
    severity = random.choice([1, 1, 2, 2, 3])

    sentinel_rows.append((
        event_id,
        event_time.strftime("%Y-%m-%d %H:%M:%S"),
        location_zone,
        event_type,
        severity
    ))

cursor.executemany("""
INSERT INTO sentinel_events VALUES (?, ?, ?, ?, ?)
""", sentinel_rows)

# Save changes
conn.commit()

# Print table counts
cursor.execute("SELECT COUNT(*) FROM rover_telemetry")
rover_count = cursor.fetchone()[0]

cursor.execute("SELECT COUNT(*) FROM rover_units")
unit_count = cursor.fetchone()[0]

cursor.execute("SELECT COUNT(*) FROM sentinel_events")
event_count = cursor.fetchone()[0]

print("\nDatabase created successfully.")
print("Database saved to:", db_path)
print("rover_telemetry rows:", rover_count)
print("rover_units rows:", unit_count)
print("sentinel_events rows:", event_count)

conn.close()