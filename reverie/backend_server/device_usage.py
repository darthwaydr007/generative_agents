import csv
from collections import Counter, defaultdict
from datetime import datetime
from utils import *  
import os

def calculate_device_usage(file_path):
    device_usage = {}

    with open(file_path, "r") as csv_file:
        reader = csv.reader(csv_file)
        headers = next(reader)
        devices = headers[1:]  # Exclude the timestamp column

        for device in devices:
            device_usage[device] = 0

        for row in reader:
            states = row[1:]
            #print(devices)
            #print(states)
            for device, state in zip(devices, states):
                if state != "idle" and state != "turned off" and state !="closed":
                    device_usage[device] += 1

    # Multiply count by 10 (assuming each row represents 10 seconds)
    for device in device_usage:
        device_usage[device] *= 10 
        #print(device , device_usage[device])
        device_usage[device] //= 60

    return device_usage
# File path to the dataset
file_path = "application_usage_final_isabella_2.csv"  # Replace with your actual file path

# Calculate and print results
device_usage = calculate_device_usage(file_path)
for device, usage_time in device_usage.items():
    print(f"{device}: {usage_time} minutes")