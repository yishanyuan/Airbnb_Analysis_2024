# Midterm_Project_2024

# Installation



# Quick Start


# Search Data
Automating the process of searching for Airbnb listings based on specified search parameters, extracting property links, and saving/loading these links for future use.

**Functions Used:** <br>
`search`: Simulates an Airbnb search with specific parameters (location, check-in, check-out dates, and guest details) and extracts property links from the results.<br>
`save_urls`: Saves the extracted property links to a JSON file.<br>
`load_urls`: Loads saved property links from a JSON file for future processing.<br>

**Processing Logic:**
The program constructs a search URL based on user input (location, check-in, check-out, etc.) and uses `Selenium` to navigate to the Airbnb results page. The HTML content of the page is parsed with `BeautifulSoup` to extract property links that contain "/rooms/". The process is repeated for all available pages by clicking the "Next" button until no more results are found. Extracted links are saved in a JSON file and can be loaded later for further use.

# Scraping Data
Automating the process of searching Airbnb property listings, extracting room details (features, prices, house rules), and saving this data into a JSON file.

**Functions Used:** <br>
`open`: Initializes the headless browser using `Selenium` WebDriver with customized options.<br>
`close`: Closes the `Selenium` WebDriver once all operations are completed.<br>
`search`: Searches for property links based on specified parameters (location, check-in, check-out).<br>
`save_urls`: Saves the collected property links into a JSON file.<br>
`load_urls`: Loads previously saved property links from a JSON file.<br>
`get_room_details_page`: Loads and parses the room details page using `BeautifulSoup`.<br>
`extract_room_features`, `extract_price_info`, `extract_house_rules`: Extract room features, pricing details, and house rules respectively from each property page.<br>
`save_to_json`: Saves the extracted room details into a JSON file.<br>

**Processing Logic:**
The program starts by opening a headless browser using `Selenium` WebDriver. It performs a search for property listings based on specified cities and check-in/check-out dates. Property links are extracted, and they can be saved to or loaded from a JSON file. For each property link, the page is loaded, and details such as room features, prices, and house rules are extracted. The extracted data is stored in a dictionary and saved into a JSON file for further use. After completing the extraction process, the browser is closed.


# Extract Data
Extracting detailed information about Airbnb properties (room features, prices, and house rules) from property URLs and saving this information into a JSON file.

**Functions Used:** <br>
`get_room_details_page`: Loads and parses the room details page using `BeautifulSoup` after interacting with the webpage (e.g., closing popups).<br>
`extract_room_features`: Extracts room features by clicking the "Show all amenities" button and parsing the content.<br>
`extract_price_info`: Extracts pricing information including nightly rates, cleaning fees, and other costs from the room details page.<br>
`extract_house_rules`: Extracts the house rules of a room by clicking the "Show more" button and parsing the content.<br>
`save_to_json`: Saves the extracted room details into a JSON file for further use.<br>

**Processing Logic:**
For each property URL, the page is loaded and any popups (like translation prompts) are closed. `BeautifulSoup` is then used to parse the page's HTML content, and relevant room details (features, prices, house rules) are extracted. Room features are retrieved by interacting with a "Show all amenities" button, while price information is obtained from specific sections on the page. House rules are similarly extracted by interacting with a "Show more" button. Finally, all extracted data is saved into a JSON file for future processing or analysis.


# Clean Data
Using the `python3 code/cleaned_data.py` on the cmd to run the data.

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

**Description**

This script updates an existing CSV file by adding new columns such as Smoking allowed, Pets allowed, and Free parking. It also adds a Length of lease column based on the check-out date, marking rows as one day, one week, or one month.

**Workflow**

The workflow includes reading the input CSV file (e.g., path_to_your_existing_csv_file.csv) from the data folder, scanning the Features column to check for Smoking allowed, Pets allowed, and Free parking, adding corresponding columns to indicate whether these features are available, adding a Length of lease column based on specific check-out dates, and saving the updated CSV file to the data folder.

## Data Processing and Price Adjustment Script (sort_into_different_time_files.py，split_data.py) ##

**Description**

This script updates the Length of lease based on Check In and Check Out dates and adjusts prices for records with a length of lease as one week and one month. It also splits the data into three separate files based on the length of lease: one day, one week, and one month. The processed data is saved as Excel files.

**Workflow**

The workflow includes reading the input CSV file, updating the Length of lease based on Check In and Check Out dates, deleting unnecessary columns like Cleaning Fee and Airbnb Service Fee, splitting the data into three files based on the Length of lease, and saving the processed data as Excel files while adjusting the column widths for date columns.

# Visualization Data
tianyi
