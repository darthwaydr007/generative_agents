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
    location = description.split("@")[1].rsplit(":", 1)[0].strip()
    # location = location.split()[-1]
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
    def extract_unique_values(data, index):
        return {row[index] for row in data}

    # Get unique values for location
    unique_values = extract_unique_values(data_rows, 5)
    # location_map = {'tv', 'desk', 'kitchen sink', 'bed', 'shelf', 'refrigerator', 'piano', 'cooking area', 
    #                 'behind the cafe counter', 'cafe customer seating', 'furnace', 'coffee machine', 'shower',
    #                 'bathroom sink', 'closet'}
    map_location = {"the Ville:Maria Lopez's apartment": {(12, 4), (12, 1), (3, 4), (4, 3), (3, 1), (5, 4), (5, 1), (9, 2), (0, 2), (11, 2), (8, 3), (8, 6), (2, 2), (13, 2), (10, 3), (1, 3), (7, 4), (6, 2), (7, 1), (4, 2), (12, 3), (3, 3), (5, 3), (8, 2), (9, 1), (11, 4), (10, 2), (9, 4), (0, 1), (11, 1), (2, 4), (1, 2), (0, 4), (2, 1), (13, 1), (13, 4), (6, 1), (6, 4), (7, 3), (7, 6), (12, 2), (3, 2), (4, 1), (5, 2), (4, 4), (8, 4), (9, 3), (8, 1), (10, 4), (1, 1), (0, 3), (10, 1), (11, 3), (1, 4), (8, 5), (2, 3), (13, 3), (7, 2), (7, 5), (6, 3)}, 
                    "the Ville:Maria Lopez's apartment:main room": {(3, 4), (4, 3), (3, 1), (5, 4), (5, 1), (8, 3), (8, 6), (2, 2), (1, 3), (7, 4), (6, 2), (7, 1), (4, 2), (3, 3), (5, 3), (8, 2), (8, 5), (9, 4), (2, 4), (1, 2), (2, 1), (6, 1), (6, 4), (7, 3), (7, 6), (3, 2), (4, 1), (5, 2), (4, 4), (8, 4), (8, 1), (1, 1), (1, 4), (2, 3), (7, 2), (7, 5), (6, 3)}, 
                    "the Ville:Maria Lopez's apartment:bathroom": {(11, 1), (12, 4), (12, 1), (10, 4), (11, 3), (10, 1), (12, 3), (11, 2), (12, 2), (10, 3), (11, 4), (10, 2)},
                    'the Ville:Hobbs Cafe:cafe': {(4, 9), (3, 13), (5, 10), (8, 9), (9, 8), (11, 14), (2, 11), (6, 11), (7, 10), (5, 12), (8, 11), (9, 10), (11, 7), (1, 8), (6, 13), (7, 12), (3, 8), (5, 14), (9, 12), (11, 9), (1, 10), (7, 14), (12, 13), (3, 10), (5, 7), (9, 14), (1, 12), (7, 7), (3, 12), (5, 9), (4, 11), (9, 7), (10, 8), (1, 14), (2, 13), (7, 9), (12, 8), (3, 14), (5, 11), (4, 13), (9, 9), (8, 13), (10, 10), (1, 7), (7, 11), (12, 10), (3, 7), (5, 13), (10, 12), (1, 9), (11, 11), (2, 8), (6, 8), (12, 12), (3, 9), (4, 8), (8, 8), (10, 14), (1, 11), (11, 13), (2, 10), (6, 10), (12, 14), (3, 11), (4, 10), (8, 10), (10, 7), (1, 13), (2, 12), (6, 12), (12, 7), (4, 12), (8, 12), (10, 9), (9, 11), (11, 8), (2, 14), (6, 14), (7, 13), (12, 9), (4, 14), (8, 14), (10, 11), (9, 13), (11, 10), (2, 7), (6, 7), (12, 11), (4, 7), (5, 8), (8, 7), (10, 13), (11, 12), (2, 9), (6, 9), (7, 8)}}
    
    inverse_map_location = {}
    for obj, coords in map_location.items():
        for coord in coords:
            inverse_map_location[coord] = obj
    print("inverse map location")
    print(inverse_map_location)

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
    print("inverse coordinates")
    print(inverse_coordinates)
    
    for row in data_rows:
        x,y = row[2] , row[3]
        object = row[5]
        row[4] = inverse_map_location[(x,y)]
        if (x,y) in inverse_coordinates:
            row[5] = inverse_coordinates[(x,y)]
        else:
            row[5] = ''

        # if (x,y) not in coordinates[object]:
        #     row[6] = 'Walking'
    
    print(data_rows[:5])
    print("data_rows")
    print(data_rows[360:380])

    # Write sorted data to CSV
    
    with open(output_file, mode="w", newline="", encoding="utf-8") as csvfile:
        writer = csv.writer(csvfile)
        writer.writerow(["Date", "Time", "Movement_X", "Movement_Y", "Location", "Object", "Action"])
        writer.writerows(data_rows)

    print(f"Data has been sorted and saved to {output_file}.")

    print(f"Data has been extracted to {output_file}.")

if __name__ == "__main__":
    main()
