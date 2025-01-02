import csv
from collections import Counter, defaultdict
from datetime import timedelta
from utils import *  
import os

def analyze_csv(file_path):
    """Perform advanced data analysis on the CSV."""
    device_states = {}
    state_counts = Counter()
    active_time = Counter()
    state_transitions = defaultdict(lambda: Counter())
    concurrent_activity = []

    with open(file_path, mode='r', encoding='utf-8') as csvfile:
        reader = csv.DictReader(csvfile)
        timestamps = []

        # Parse rows
        for row in reader:
            #timestamps.append(row["timestamp"])
            active_devices = 0

            for device, state in row.items():
                if device == "timestamp":
                    continue

                # Track device states and transitions
                if device not in device_states:
                    device_states[device] = []
                if device_states[device]:
                    prev_state = device_states[device][-1]
                    if prev_state != state:
                        state_transitions[device][f"{prev_state} → {state}"] += 1
                device_states[device].append(state)
                
                # Update active time
                if state not in ["idle", "turn off"]:
                    active_time[device] += 1
                    active_devices += 1

            # Track concurrent active devices
            concurrent_activity.append(active_devices)

    # Analyze data
    interval = 10  # Time interval in seconds
    total_entries = len(timestamps)
    print(f"Total data points: {total_entries}")

    # State Frequencies
    print("\nDevice State Frequencies:")
    for device, states in device_states.items():
        state_count = Counter(states)
        for state, count in state_count.items():
            state_counts[(device, state)] += count
            print(f"{device} - {state}: {count} times")

    # Active Time in Seconds
    print("\nDevice Active Time (in seconds):")
    for device, time in active_time.items():
        print(f"{device}: {time * interval} seconds")

    # State Transitions
    print("\nDevice State Transitions:")
    for device, transitions in state_transitions.items():
        print(f"{device}:")
        for transition, count in transitions.items():
            print(f"  {transition}: {count} times")

    # Longest Active Period
    print("\nLongest Active Periods:")
    for device, states in device_states.items():
        max_active = 0
        current_active = 0
        for state in states:
            if state not in ["idle", "turn off"]:
                current_active += 1
                max_active = max(max_active, current_active)
            else:
                current_active = 0
        print(f"{device}: {max_active * interval} seconds")

    # Concurrent Active Devices
    print("\nConcurrent Active Devices:")
#    print(f"Average: {sum(concurrent_activity) / total_entries:.2f}")
#    print(f"Peak: {max(concurrent_activity)} devices")

def main():
    # Input CSV file path
    # Input folder and validate
    folder = input("Enter the folder name: ").strip()

    # Construct the directory and file paths
    # Replace with actual path
    directory = f"{fs_storage}/{folder}/movement"
    print(f"Directory: {directory}")

    if not os.path.isdir(directory):
        print("Invalid directory. Please check the path and try again.")
        exit()

    file_path = f"smart_home_status_test_{folder}.csv"
    output_file = f"activity_device_analysis_{folder}.txt"
    #file_path = "device_data.csv"  # Replace with your CSV file path

    analyze_csv(file_path)

if __name__ == "__main__":
    main()
