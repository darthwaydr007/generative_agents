import json
import csv
from datetime import datetime
import os
from global_methods import *  
from utils import *           
from maze import *            
from persona.persona import * 

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
rows.sort(key=lambda x: (x["timestamp"]))

# Prepare CSV header
header = ["timestamp"] + sorted(devices)

# Create the CSV rows with default status 'off' and persistent state
timestamps = {}
device_states = {device: "idle" for device in devices}  # Initial state for all devices
#prev_state = {device: "off" for device in devices}
for row in rows:
    timestamp = row["timestamp"]
    device = row["device"]
    status = row["status"]

    # Update the device state
    # if status != "idle":  # Update only if the status is not idle
    #     device_states[device] = status
    # elif device_states[device] != "off":  # Reset to off only if the current state is idle
    #     device_states[device] = "off"
    print(device_states["furnace"] , device, status)
    print(device_states)
    # if device_states[device] != "idle" or device_states[device] != "off":
    #     device_states[device] = status

    if timestamp not in timestamps:
        timestamps[timestamp] = {"timestamp": timestamp}
    for dev in devices:
    #need to handle case for each device
        if dev == device and status!= "idle":
            timestamps[timestamp][dev] = status #device_states[dev]
            device_states[dev] = status
        else:
            timestamps[timestamp][dev] = device_states[dev]
    #prev_state[device] = status

# Populate the final rows for the CSV
csv_rows = [timestamps[key] for key in sorted(timestamps)]

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
