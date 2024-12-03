import json
import os
from datetime import datetime, timedelta
from global_methods import *  
from utils import *           
from maze import *            
from persona.persona import * 

from datetime import datetime

import csv

def json_to_csv(json_data, output_csv):
    """Convert JSON data to a CSV file."""
    if not json_data:
        print("No data to write.")
        return

    # Extract fieldnames from keys of the first dictionary
    fieldnames = list(json_data[0].keys())

    # Write to CSV
    try:
        with open(output_csv, mode="w", newline="", encoding="utf-8") as csvfile:
            writer = csv.DictWriter(csvfile, fieldnames=fieldnames)
            writer.writeheader()  # Write the header
            writer.writerows(json_data)  # Write the rows
        print(f"CSV file '{output_csv}' created successfully.")
    except IOError as e:
        print(f"Error writing to CSV: {e}")

# Example usage


def generate_timestamps(start, end, gap=10):
    start_time = datetime.strptime(start, "%Y-%m-%d %H:%M:%S")
    end_time = datetime.strptime(end, "%Y-%m-%d %H:%M:%S")
    timestamps = []
    while start_time < end_time:  # Generate timestamps up to, but not including, end
        timestamps.append(start_time.strftime("%Y-%m-%d %H:%M:%S"))
        start_time += timedelta(seconds=gap)
    timestamps.append(end_time.strftime("%Y-%m-%d %H:%M:%S"))  # Include the end timestamp
    return timestamps

# Get folder name from user
folder = input("Enter the folder name: ").strip()

# Construct the file path
file_path = f"{fs_storage}/{folder}/personas/Isabella Rodriguez/bootstrap_memory/associative_memory/nodes.json"
#ALLOWED_DEVICES = {"bathroom sink", "bed", "cafe customer seating", "closet", "coffee machine", "cooking area", "desk", "furnace", "kitchen sink", "piano", "refrigerator", "shelf", "shower", "toilet", "tv"}
ALLOWED_DEVICES ={"furnace", "shower", "tv", "piano", "kitchen sink", "refrigerator", "coffee machine", "bathroom sink"}
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

# Prepare a list for rows and a set for devices
rows = []
devices = set()

# Parse JSON data
for node_id, node in data.items():
    try:
        timestamp = node["created"]
        subject = node["subject"].split(":")[-1]  # Extract device name
        description = node.get("description", "")
        predicate = node.get("predicate", "")
        obj = node.get("object", "")
        #status = predicate
        ############# DESCRIPTORS FOR STATUS ##############
        device = subject
        status = f"{description}||{predicate}||{obj}"
        if device == "furnace":
            if "use" in predicate or "provide" in predicate or "on" in predicate:
                status = "turn on"
            elif "off" in predicate:
                status = "turn off"
            else:
                status = f"{predicate}"
            
            pass
        elif device == "shower":
            status = f"{obj}"
            pass
        elif device == "tv":
            if "display" in predicate:
                status = "menu displayed"
            else:
                status = f"{predicate}"
            pass
        elif device == "piano":
            status = f"{obj}"
            pass
        elif device == "kitchen sink":
            if "clean" in description:
                status = "cleaning"
            elif "wash" in description:
                status = "washing"
            else:
                status = "idle"
            pass
        elif device == "refrigerator":
            if obj != "idle":
                status = "opened"
            else:
                status = "idle"
            pass
        elif device == "coffee machine":
            if "ready" in description or  "functioning" in description or "brew" in description:
                status = "brewing"
            else:
                status = "turn off"
            pass
        elif device == "bathroom sink":
            status = f"{obj}"
            if "Isabella" in status:
                status = "in use"
            pass
        elif device == "bed":
            status = f"{obj}"
            pass
        else:
            status = f"{description}||{predicate}||{obj}"
        ###################################################
        if subject in ALLOWED_DEVICES:  # Filter by allowed devices
            devices.add(subject)
            rows.append({"timestamp": timestamp, "device": subject, "status": status})
    except KeyError as e:
        print(f"Missing key in node {node_id}: {e}")
        continue

# Sort rows by timestamp
rows.sort(key=lambda x: x["timestamp"])

# Initialize states
device_states = {device: "idle" for device in devices}  # Default state for all devices
uniform_rows = []

# # Process rows to track the latest device states
# for row in rows:
#     device_states[row["device"]] = row["status"]
#     uniform_rows.append({
#         "timestamp": row["timestamp"],
#         **{dev: device_states[dev] for dev in devices}
#     })

# Generate intermediate timestamps after processing all rows
final_rows = []
timestamps = {}
for i in range(len(rows)):
    current_row = rows[i]
    
    current_timestamp = current_row["timestamp"]
    device = current_row["device"]
    status = current_row["status"]
    
    # Ensure timestamp is recorded and initialized with current states if new
    if current_timestamp not in timestamps:
        timestamps[current_timestamp] = device_states.copy()

    # Update the state of the specific device
    for dev in devices:
        if dev == device:
            if status == "is":
                timestamps[current_timestamp][dev] = device_states[dev]
            else:
                timestamps[current_timestamp][dev] = status
                device_states[dev] = status
    final_rows.append({"timestamp": current_timestamp, **device_states})

#print(timestamps)
sorted_timestamps = sorted(timestamps.keys(), key=lambda x: datetime.strptime(x, "%Y-%m-%d %H:%M:%S"))

uniform_rows = []
for i in range(len(final_rows) - 1):
    current_time = final_rows[i]["timestamp"]
    current_state = final_rows[i]
    print(current_time)
    print(current_state)
    break
    
#       

final_rows1 = []  # This will store the final rows

# Sort the timestamps keys to ensure chronological order
sorted_timestamps = sorted(timestamps.keys(), key=lambda x: datetime.strptime(x, "%Y-%m-%d %H:%M:%S"))

for i, timestamp in enumerate(sorted_timestamps[1:], start=1):  # Start from index 1
    current_time = datetime.strptime(timestamp, "%Y-%m-%d %H:%M:%S")
    previous_time = datetime.strptime(sorted_timestamps[i - 1], "%Y-%m-%d %H:%M:%S")  # Get the previous timestamp

    # Get the device state of the previous timestamp
    previous_device_state = timestamps[sorted_timestamps[i - 1]]

    # If there's a gap between the previous timestamp and current one
    while (previous_time + timedelta(seconds=10)) < current_time:
        previous_time += timedelta(seconds=10)
        intermediate_timestamp = previous_time.strftime("%Y-%m-%d %H:%M:%S")

        # Add intermediate row with the previous timestamp's device state
        final_rows1.append({"timestamp": intermediate_timestamp, **previous_device_state})

    # Add the current timestamp row
    final_rows1.append({"timestamp": timestamp, **timestamps[timestamp]})
# for i, timestamp in enumerate(timestamps):
#     current_time = datetime.strptime(timestamp, "%Y-%m-%d %H:%M:%S")
    
#     if previous_time:
#         # Add rows for intermediate timestamps
#         while (previous_time + timedelta(seconds=10)) < current_time:
#             previous_time += timedelta(seconds=10)
#             intermediate_timestamp = previous_time.strftime("%Y-%m-%d %H:%M:%S")
#             final_rows.append({"timestamp": intermediate_timestamp, **device_states})

#     # Add the current timestamp row
#     final_rows.append({"timestamp": timestamp, **timestamps[timestamp]})
#     previous_time = current_time

# Define the output file name
output_file = f"smart_home_status_test_{folder}.json"

# Write to JSON
try:
    with open(output_file, "w") as file:
        json.dump(final_rows1, file, indent=4)
    print(f"JSON file '{output_file}' created successfully in the current directory.")
except IOError as e:
    print(f"Error writing to file: {e}")

output_csv_file = f"smart_home_status_test_{folder}.csv"

# Assuming `final_rows` is generated from the previous step
json_to_csv(final_rows1, output_csv_file)

