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

    # Extract fieldnames from keys of the first dictionary, splitting timestamp
    fieldnames = ["Date", "Time"] + [key for key in json_data[0].keys() if key != "timestamp"]

    # Write to CSV
    try:
        with open(output_csv, mode="w", newline="", encoding="utf-8") as csvfile:
            writer = csv.DictWriter(csvfile, fieldnames=fieldnames)
            writer.writeheader()  # Write the header

            for row in json_data:
                # Split the timestamp into Date and Time
                date, time = row["timestamp"].split(" ")
                # Exclude the original timestamp and add Date and Time
                row_data = {"Date": date, "Time": time}
                row_data.update({key: row[key] for key in row if key != "timestamp"})
                writer.writerow(row_data)

        print(f"CSV file '{output_csv}' created successfully with Date and Time columns.")
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
#file_path = f"{fs_storage}/{folder}/personas/Isabella Rodriguez/bootstrap_memory/associative_memory/nodes.json"
file_path = f"{fs_storage}/{folder}/personas/Maria Lopez/bootstrap_memory/associative_memory/nodes.json"

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
        subject = node["subject"].split(":")[-1].lower()  # Extract device name
        description = node.get("description", "").lower()
        predicate = node.get("predicate", "").lower()
        obj = node.get("object", "").lower()
        device = subject
        for x in ALLOWED_DEVICES:
            if x in subject or x in obj:
                
                device = x
                #if device == "tv":
                    #print(device , node)
                break
        # if node["type"] == "event" and ("TV" in str(node) or "tv" in str(node)):
        #     print(timestamp , node)
            
        #status = predicate
        ############# DESCRIPTORS FOR STATUS ##############
        
        
        status = f"{description}||{predicate}||{obj}"
        
        if device == "furnace":
            if "use" in predicate or "provide" in predicate or "on" in predicate:
                status = "turned on"
            elif "off" in predicate:
                status = "turned off"
            else:
                status = f"{predicate}"
            pass
        elif device == "shower":
            status = f"{obj}"
            if status != "idle" or "use" in description:
                status = "in use"
            pass
        elif  device == "tv":
            #print(timestamp , 'tv' , status)
            if "display" in predicate or "on" in predicate or "on" in description:
                status = "turned on"
                print("HOTTTTTTTT" , timestamp , status)
            elif  "off" in predicate:
                status = "turned off"
            else:
                status = f"{predicate}"
            pass
        elif device == "piano":
            status = f"{obj}"
            pass
        elif device == "kitchen sink":
            if "clean" in description:
                status = "in use"
            elif "wash" in description or "warm" in status or "use" in description:
                status = "in use"
            else:
                status = "idle"
            pass
        elif device == "refrigerator":
            if obj != "idle":
                status = "open"
            else:
                status = "idle"
            pass
        elif device == "coffee machine":
            if "ready" in description or  "functioning" in description or "brew" in description:
                status = "turned on"
            else:
                status = "turned off"
            pass
        elif device == "bathroom sink":
            status = f"{obj}"
            if "Maria" in status or "warm" in status or "use" in description:
                status = "in use"
            pass
        elif device == "bed":
            status = f"{obj}"
            pass
        else:
            status = f"{description}||{predicate}||{obj}"
        ###################################################
        for x in ALLOWED_DEVICES:
            if x in subject.lower() or x in obj.lower():  # Filter by allowed devices
                devices.add(x)
                rows.append({"timestamp": timestamp, "device": x, "status": status})
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
    if device == "tv":
        print(current_timestamp , device , status)
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
#print(final_rows1[:5])
def create_map_from_csv(csv_file_path):
    timestamp_map = {}

    with open(csv_file_path, mode='r') as file:
        csv_reader = csv.DictReader(file)  # Use DictReader for easy access to column names
        
        for row in csv_reader:
            # Combine Date and Time columns for the key
            timestamp = f"{row['Date']} {row['Time']}"
            
            # Add the (Movement_X, Movement_Y) pair to the map
            x, y , obj = int(row['Movement_X']), int(row['Movement_Y']) ,row["Object"] 
            timestamp_map[timestamp] = (x, y , obj)

    return timestamp_map

# Example usage
csv_file_path = f"activity_data_{folder}.csv"  # Replace with the path to your CSV file
movement_data = create_map_from_csv(csv_file_path)
# for i, key in enumerate(movement_data.keys()):
#     if i == 5:  # Stop after 5 keys
#         break
#     print(type(key))
#     print(key , movement_data[key])






coordinates = {'bed': {(1, 2), (2, 2)}, 'refrigerator': {(1, 7), (2, 7)}, 'closet': {(6, 2), (5, 2)}, 
                   'shelf': {(8, 2), (7, 2)}, 'shower': {(11, 2), (10, 2)}, 'desk': {(2, 4)}, 'bathroom sink': {(11, 4)},
                    'cooking area': {(4, 7), (5, 7)}, 'kitchen sink': {(6, 7)}, 
                    'behind the cafe counter': {(8, 7), (9, 7), (10, 7), (7, 7)},
                    'furnace': {(3, 8), (3, 9), (3, 10)}, 'cafe customer seating': {(7, 9), (3, 13), (1, 13), (9, 9), (1, 11), (11, 9), (3, 11)}, 
                    'coffee machine': {(12, 9)}, 'tv': {(6, 13), (7, 13)}, 'piano': {(11, 14), (12, 14)}}
    
inverse_coordinates = {}
for obj, coords in coordinates.items():
    for coord in coords:
        inverse_coordinates[coord] = obj

# x = final_rows1[:5]
# print(x)
cnt = 0
contact_appliances = ('refrigerator', 'piano', 'shower', 'kitchen sink', 'coffee machine' , 'bathroom sink' )
for i in range(len(final_rows1)):
    date = final_rows1[i]['timestamp']
    (x,y,obj_m) = movement_data[date]
    
    if (x,y) in inverse_coordinates:
        obj = inverse_coordinates[(x,y)]
        for app in contact_appliances:
            state = final_rows1[i][app]
                
            if state != 'idle':
                if app == obj and app  == obj_m:
                    if obj_m == "shower":
                        print(date, x , y , obj_m , obj , state)
                        cnt+=1
                    final_rows1[i][app] = 'in use'
                else:
                    final_rows1[i][app] = 'idle'
    else:
        for app in contact_appliances:
            final_rows1[i][app] = 'idle'
turned_off_appliances = ('tv', 'furnace', 'coffee machine')
#, 'refrigerator'
for i in range(len(final_rows1)):
    if final_rows1[i]['refrigerator'] == 'idle':
        final_rows1[i]['refrigerator'] = 'closed'
    for app in turned_off_appliances:
        if final_rows1[i][app] == 'idle':
            final_rows1[i][app] = 'turned off'
        if final_rows1[i][app] =='be adjusted' or final_rows1[i][app] == 'use':
            final_rows1[i][app] = 'turned on'
state_set = set()
for i in range(len(final_rows1)):
    for app in ALLOWED_DEVICES:
        state_set.add( final_rows1[i][app])
print(state_set)


        



        

print('shower count ' , cnt)
output_file = f"application_usage_{folder}.json"

# Write to JSON
try:
    with open(output_file, "w") as file:
        json.dump(final_rows1, file, indent=4)
    print(f"JSON file '{output_file}' created successfully in the current directory.")
except IOError as e:
    print(f"Error writing to file: {e}")

output_csv_file = f"application_usage_{folder}.csv"

# Assuming `final_rows` is generated from the previous step
json_to_csv(final_rows1, output_csv_file)

