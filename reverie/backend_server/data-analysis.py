import os
import pandas as pd
import numpy as np
from utils import *   
from datetime import datetime

# Input folder and validate
folder = input("Enter the folder name: ").strip()

# Construct the directory and file paths
directory = f"{fs_storage}/{folder}/movement"
print(f"Directory: {directory}")

if not os.path.isdir(directory):
    print("Invalid directory. Please check the path and try again.")
    exit()

file_path = f"activity_data_{folder}.csv"
output_file = f"activity_data_analysis_{folder}.csv"

# Load the CSV file into a DataFrame
df = pd.read_csv(file_path)

# Function to calculate distance
def calculate_distance(row1, row2):
    return np.sqrt((row2['Movement_X'] - row1['Movement_X'])**2 + (row2['Movement_Y'] - row1['Movement_Y'])**2)

# 1. Calculate total distance traveled
total_distance = sum(
    calculate_distance(df.iloc[i], df.iloc[i + 1])
    for i in range(len(df) - 1)
)

# 2. Time spent in each location
df['Datetime'] = pd.to_datetime(df['Date'] + ' ' + df['Time'])  # Combine Date and Time
df['Time_Difference'] = df['Datetime'].diff().dt.total_seconds()  # Time difference in seconds
time_spent = df.groupby('Location')['Time_Difference'].sum()

# 3. Number of times each action is performed
action_count = df['Action'].value_counts()

# 4. List of unique actions performed
unique_actions = df['Action'].unique()

# 5. Average time spent per location
average_time_spent = time_spent / df['Location'].value_counts()

# 6. Action transition counts
action_transitions = df['Action'].shift(1) + " → " + df['Action']
transition_counts = action_transitions.value_counts()

# 7. Most frequent location
most_frequent_location = df['Location'].value_counts().idxmax()

# 8. Longest time spent in a single location
longest_time_spent = df.groupby('Location')['Time_Difference'].max()

# 9. Heatmap of movement (data preparation for visualization)
movement_heatmap = df.groupby(['Movement_X', 'Movement_Y']).size().unstack(fill_value=0)

# Write results to a text file
with open(output_file, "w") as file:
    file.write(f"Total distance traveled: {total_distance:.2f} units\n\n")
    
    file.write("Time spent in each location (in seconds):\n")
    file.write(time_spent.to_string() + "\n\n")
    
    
    
    # file.write("List of unique actions performed:\n")
    # file.write(", ".join(unique_actions) + "\n\n")
    
    file.write("Average time spent in each location (in seconds):\n")
    file.write(average_time_spent.to_string() + "\n\n")
    
   
    
    file.write(f"Most frequent location: {most_frequent_location}\n\n")
    
    file.write("Number of times each action is performed:\n")
    file.write(action_count.to_string() + "\n\n")

    file.write("Action transition counts:\n")
    file.write(transition_counts.to_string() + "\n\n")



print(f"Analysis results have been saved to {output_file}")

