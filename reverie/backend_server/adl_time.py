import csv
from collections import defaultdict
import re

# Load dataset and calculate activity counts and durations
def calculate_activity_data(file_path):
    activity_data = defaultdict(lambda: {"count": 0, "total_time": 0})

    with open(file_path, "r") as csv_file:
        reader = csv.reader(csv_file)
        headers = next(reader)

        for row in reader:
            activity = row[6]  # Action column
            # Extract text inside parentheses
            match = re.search(r"\((.*?)\)", activity)
            if match:
                activity = match.group(1)
            activity_data[activity]["count"] += 1

        for activity in activity_data:
            # Multiply count by 10 to get total time (assuming each row represents 10 seconds)
            activity_data[activity]["total_time"] = activity_data[activity]["count"] * 10

    return activity_data

# File path to the dataset

def save_activity_data_to_csv(activity_data, output_file):
    with open(output_file, "w", newline="") as csv_file:
        writer = csv.writer(csv_file)
        writer.writerow(["Activity", "Count", "Total Time (seconds)"])

        for activity, data in activity_data.items():
            writer.writerow([activity, data["count"], data["total_time"]])

# File path to the dataset
file_path = "activity_data_final_isabella_2.csv"  # Replace with your actual file path

output_file = "activity_summary_final_isabella_2.csv"  # Output file for results

# Calculate and save results
activity_data = calculate_activity_data(file_path)
save_activity_data_to_csv(activity_data, output_file)

print(f"Activity data saved to {output_file}")