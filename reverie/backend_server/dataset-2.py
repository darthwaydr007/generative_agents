import os
import json
import csv
from global_methods import *  
from utils import *           
from maze import *            
from persona.persona import * 
from datetime import datetime

def extract_device_status(json_data):
    """Extract the device status from the JSON data."""
    devices = {}  # Dictionary to store device statuses
    
    for node_key, node_value in json_data.items():
        # Extract timestamp
        timestamp = node_value.get("created", None)
        if not timestamp:
            continue

        # Extract device name (last part of subject)
        subject = node_value.get("subject", "")
        device_name = subject.split(":")[-1] if ":" in subject else subject

        # Extract device status
        description = node_value.get("description", "")
        predicate = node_value.get("predicate", "")
        obj = node_value.get("object", "")
        status = (description or predicate or obj).strip()  # Fallback to available fields

        # Save the device status
        devices[device_name] = status

    return devices

def generate_csv(activity_file, output_file, device_list):
    """Generate the CSV file."""
    with open(activity_file, "r", encoding="utf-8") as f:
        json_data = json.load(f)
    
    # Extract all device statuses
    devices_status = extract_device_status(json_data)

    # Create a CSV with the format
    with open(output_file, mode="w", newline="", encoding="utf-8") as csvfile:
        writer = csv.writer(csvfile)
        
        # Write header
        header = ["timestamp"] + device_list
        writer.writerow(header)
        
        # Write row for each timestamp
        for timestamp, status in devices_status.items():
            row = [timestamp] + [devices_status.get(device, "idle") for device in device_list]
            writer.writerow(row)

if __name__ == "__main__":
    # Example inputs
    activity_dataset =  f"{fs_storage}/the_room3-1/personas/Isabella Rodriguez/bootstrap_memory/associative_memory/nodes.json"
  # Input JSON file
    output_csv = "smart-home-test.csv"  # Output CSV file
    allowed_devices = ["bathroom sink", "bed", "cafe customer seating", "closet", "coffee machine", "cooking area", "desk", "furnace", "kitchen sink", "piano", "refrigerator", "shelf", "shower", "toilet", "tv"]  # List of devices

    generate_csv(activity_dataset, output_csv, allowed_devices)
