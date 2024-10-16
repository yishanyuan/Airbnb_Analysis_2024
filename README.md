# Midterm_Project_2024

# Installation

Using the `python3 code/cleaned_data.py` on the cmd to run the data.

# Quick Start

# Scrape Data
yishan

# Clean Data

## Extract Check-in and Check-out Dates from URLs
Using regular expressions to extract the check_in and check_out dates from each listing's URL and adds these dates to the listing details.

**Regular Expression Pattern:** The pattern `r'check_in=(\d{4}-\d{2}-\d{2})&check_out=(\d{4}-\d{2}-\d{2})'` matches URLs containing dates such as check_in=2024-11-01&check_out=2024-11-05.
If a match is found, the two dates (check_in and check_out) are captured.


**Processing Logic:** Iterate through all the listings, checking each URL for a match.
If the dates are found, add them to the corresponding listing details.
Store the updated listings in a new dictionary for further processing.

## Assign Cities Based on Check-out Dates
Assigning cities to each listing based on specific check-out dates. When certain dates are encountered, the city is switched to the next one in the predefined list.

**Key dates:** When the check_out date is `"2024-11-30"`, it signals the start of a new batch.
If `"2024-11-02"` is encountered after this batch starts, the city assignment will rotate to the next city.

**City List:** The predefined city list is: `["Austin, TX", "New York City, NY", "Chicago, IL", "Los Angeles, CA"].`
The logic rotates through the list using city indexes, updating the assigned city whenever the key dates trigger a rotation.

**Processing Logic:** Initialize the city index to 0 (pointing to the first city, Austin, TX).
Iterate through the listings:
If the check_out date is `"2024-11-30"`, mark it as a new batch.
If `"2024-11-02"` is found within the new batch, advance the city index to the next city.
Assign the city corresponding to the current index to each listing.


## Remove Invalid Records
The valid data is retained by applying several filtering conditions:

**Filtering Conditions:** The URL must start with `https`. Otherwise, the listing is removed.
features, prices, and house_rules must all contain valid data. If any of these fields are empty, the listing is discarded.

**Processing Logic:** Iterate through the listings, checking if each URL starts with https.
Use the `len()` function to ensure that features, prices, and house_rules are not empty.
If a listing meets all the criteria, it is added to the cleaned data dictionary.

## Load and Save JSON Data
The program includes functions to load data from a JSON file and save the processed data into a new JSON file.

# Manipulate Data

## JSON to CSV Conversion Script (Change_file_format.py) ##

This script converts processed JSON files (e.g., cleaned_data.json) into CSV files. It reads data from a JSON file, extracts fields such as URL, city, check-in/check-out dates, features, and price details, and writes the data into CSV format. The generated CSV file is saved in the data folder. The workflow involves reading JSON data from cleaned_data.json, extracting fields like city, check-in/check-out dates, features, and prices, converting the data into CSV format, and saving the output CSV file (e.g., output_data.csv) to the data folder.

## CSV Enhancement Script (manipulated_variables.py) ##

This script updates an existing CSV file by adding new columns such as Smoking allowed, Pets allowed, and Free parking. Additionally, it adds a Length of lease column based on the check-out date, marking rows as one day, one week, or one month.

	•	Workflow:
	•	Read the input CSV file (e.g., path_to_your_existing_csv_file.csv) from the data folder.
	•	Scan the Features column to check for Smoking allowed, Pets allowed, and Free parking.
	•	Add corresponding columns to indicate whether these features are available.
	•	Add a Length of lease column, marking as one day, one week, or one month based on specific check-out dates.
	•	Save the updated CSV file to the data folder.

## Data Processing and Price Adjustment Script (sort_into_different_time_files.py) ##

This script updates the Length of lease based on Check In and Check Out dates and adjusts prices for records with a length of lease as one week and one month. The processed data is saved as an Excel file.

	•	Workflow:
	•	Read the input CSV file.
	•	Update the Length of lease based on Check In and Check Out dates.
	•	Delete unnecessary columns (e.g., Cleaning Fee and Airbnb Service Fee).
	•	Save the processed data as an Excel file, adjusting the column width for date columns.

# Visualization Data
tianyi