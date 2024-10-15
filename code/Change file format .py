import json
import csv
import os

# Define the base directory for your project (up one level from the script's location)
base_dir = os.path.dirname(os.path.dirname(__file__))  # Move one level up from the current directory

# Define paths for the input JSON and output CSV located in 'data' folder
data_folder_path = os.path.join(base_dir, 'data')
json_file_path = os.path.join(data_folder_path, 'cleaned_data.json')  # JSON file in 'data' folder
csv_file_path = os.path.join(data_folder_path, 'output_data.csv')     # Output CSV in 'data' folder

# Load the JSON data
with open(json_file_path, 'r') as json_file:
    data = json.load(json_file)

# Prepare CSV file
with open(csv_file_path, 'w', newline='') as csv_file:
    writer = csv.writer(csv_file)
    
    # Write the header
    header = ["URL", "City", "Check In", "Check Out", "Features", "Price Per Night", "Cleaning Fee", "Airbnb Service Fee"]
    writer.writerow(header)
    
    # Write each row of data
    for url, details in data.items():
        row = [
            url,
            details.get("city", ""),
            details.get("check_in", ""),
            details.get("check_out", ""),
            "; ".join(details.get("features", [])),
            details.get("prices", {}).get("Original Price Per Night", ""),
            details.get("prices", {}).get("Cleaning fee", ""),
            details.get("prices", {}).get("Airbnb service fee", "")
        ]
        writer.writerow(row)

print(f"CSV file created at {csv_file_path}")