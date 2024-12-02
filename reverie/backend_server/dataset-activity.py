import os
import json
import csv
from global_methods import *  
from utils import *           
from maze import *            
from persona.persona import * 
from datetime import datetime

def extract_details(json_data):
    """Extract the required details from the JSON data."""
    #print(json_data)
    curr_time = json_data["meta"]["curr_time"]
    parsed_time = datetime.strptime(curr_time, "%B %d, %Y, %H:%M:%S")
    date = parsed_time.strftime("%Y-%m-%d")
    time = parsed_time.strftime("%H:%M:%S")

    persona_data = list(json_data["persona"].values())[0]
    movement_x, movement_y = persona_data["movement"]
    description = persona_data["description"]

    # Extract parts of the description
    location = location = description.split("@")[1].rsplit(":", 1)[0].strip()
    obj = description.split(":")[-1]
    action = description.split("@")[0].strip()

    return [date, time.strip(), movement_x, movement_y, location, obj, action]

def main():
    folder = input("Enter the folder name: ").strip()

    # Construct the file path
    directory = f"{fs_storage}/{folder}/movement"
    print(directory)

    if not os.path.isdir(directory):
        print("Invalid directory. Please check the path and try again.")
        return

    output_file = f"activity_data_{folder}.csv"

    data_rows = []

    # Read and extract data from JSON files
    for filename in os.listdir(directory):
        if filename.endswith(".json"):
            filepath = os.path.join(directory, filename)
            
            with open(filepath, "r", encoding="utf-8") as f:
                data = json.load(f)
                data_rows.append(extract_details(data))

    # Sort data by date and time
    data_rows.sort(key=lambda x: (x[0], x[1]))

    # Write sorted data to CSV
    
    with open(output_file, mode="w", newline="", encoding="utf-8") as csvfile:
        writer = csv.writer(csvfile)
        writer.writerow(["Date", "Time", "Movement_X", "Movement_Y", "Location", "Object", "Action"])
        writer.writerows(data_rows)

    print(f"Data has been sorted and saved to {output_file}.")

    print(f"Data has been extracted to {output_file}.")

if __name__ == "__main__":
    main()
