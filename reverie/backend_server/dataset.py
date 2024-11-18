import json
import csv
from datetime import datetime
import os
from global_methods import *  # Assuming these provide utility methods
from utils import *           # Assuming utility functions for file handling
from maze import *            # Maze-related functionalities
from persona.persona import * # Persona-specific functionality

# Get folder name from user
folder = input("Enter the folder name: ").strip()

# Construct the file path
file_path = f"{fs_storage}/{folder}/personas/Isabella Rodriguez/bootstrap_memory/associative_memory/nodes.json"
ALLOWED_DEVICES = {"bathroom sink", "furnace", "kitchen sink", "piano", "refrigerator", "shower", "toilet"}

# Check if the file exists
if not os.path.exists(file_path):
    print(f"Error: File not found at {file_path}")
    exit()

# Load JSON data from the file
with open(file_path, "r") as file:
    try:
        data = json.load(file)
    except json.JSONDecodeError as e:
        print(f"Error reading JSON file: {e}")
        exit()

# Prepare a list for CSV rows
rows = []
devices = set()

# Parse JSON data
for node_id, node in data.items():
    try:
        timestamp = node["created"]
        subject = node["subject"].split(":")[-1]  # Extract device name
        status = node["object"]

        if subject in ALLOWED_DEVICES:  # Filter by allowed devices
            devices.add(subject)  # Collect unique devices
            rows.append({"timestamp": timestamp, "device": subject, "status": status})
    except KeyError as e:
        print(f"Missing key in node {node_id}: {e}")
        continue

# Sort rows by timestamp
# try:
#     rows.sort(key=lambda x: datetime.strptime(x["timestamp"], "%Y-%m-%d %H:%M:%S"))
# except Exception as e:
#     print(f"Error while parsing timestamps: {e}")
#     exit()

# Prepare CSV header
header = ["timestamp"] + sorted(devices)

# Create the CSV rows with default status 'idle'
timestamps = {}
for row in rows:
    if row["timestamp"] not in timestamps:
        timestamps[row["timestamp"]] = {device: "idle" for device in devices}
        timestamps[row["timestamp"]]["timestamp"] = row["timestamp"]
    timestamps[row["timestamp"]][row["device"]] = row["status"]

# Populate the final rows for the CSV
csv_rows = list(timestamps.values())

# Define the output file name
output_file = f"smart_home_status_{folder}.csv"

# Write to CSV
try:
    with open(output_file, "w", newline="") as file:
        writer = csv.DictWriter(file, fieldnames=header)
        writer.writeheader()
        writer.writerows(csv_rows)
    print(f"CSV file '{output_file}' created successfully in the current directory.")
except IOError as e:
    print(f"Error writing to file: {e}")
