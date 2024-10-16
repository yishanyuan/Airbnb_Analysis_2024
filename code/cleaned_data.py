import re
import json

## Extract check-in and check-out from URL

def add_checkin_checkout_dates(data):
    """
    Extract the check_in and check_out dates from the URL key in the JSON object and add them to each listing's details.

    Parameters:
    data (dict): The original JSON data with the URL as each key.

    Returns:
    dict: The updated JSON data with the check_in and check_out dates.
    """
    # Use regular expression used to match check_in and check_out dates
    date_pattern = r'check_in=(\d{4}-\d{2}-\d{2})&check_out=(\d{4}-\d{2}-\d{2})'
    
    # New dictionary to store updated data
    updated_data = {}
    
    # Iterate over all URLs
    for key, value in data.items():
        match = re.search(date_pattern, key)
        if match:
            # Extraction date
            check_in, check_out = match.groups()
            # Add the new date to the value dictionary
            value['check_in'] = check_in
            value['check_out'] = check_out
        # Add the updated value back to updated_data
        updated_data[key] = value
    
    return updated_data

# Extract the property location
def assign_city_to_listings(data):
    """
    Assign properties to different cities based on the checkout date in a JSON object.

    Parameters:
    data (dict): JSON data containing property information, where the key for each property is a URL string.
    cities (list): List of city names, in the order in which they were crawled.

    Returns:
    dict: Updated JSON data with the city information for each property.
    """
    cities = ["Austin, TX", "New York City, NY", "Chicago, IL", "Los Angeles, CA"]

    city_index = 0  # Used to track the current city
    updated_data = {}  # Used to store updated data
    city_30_batch = False

    # Iterate through all URLs and details
    for key, value in data.items():
        # If the checkout date of the current listing is "2024-11-30" and has entered the next batch of data
        if value.get("check_out") == "2024-11-30":
            city_30_batch = True
        if city_30_batch and (value.get("check_out") == "2024-11-02"):
            city_30_batch = False
            city_index = city_index + 1

        # Add the city of the current listing to the listing details
        value["city"] = cities[city_index]
        updated_data[key] = value

    return updated_data

def clean_invalid_records(data):
    """
    Clear records with invalid data:
    URL does not start with https
    features is empty
    prices is empty
    house_rules is empty

    Parameters:
    data (dict): Raw JSON data.

    Returns:
    dict: Data after clearing invalid records.
    """
    cleaned_data = {}

    for url, details in data.items():
        # Check if the URL starts with https
        if not url.startswith("https"):
            continue

        # Check if features, prices and house_rules are empty
        if len(details.get("features")) == 0 or len(details.get("prices")) == 0 or len(details.get("house_rules")) == 0:
            continue

        # If the record is valid, it is added to cleaned_data
        cleaned_data[url] = details

    return cleaned_data

json_file_path = "../data/file.json"

def load_json_from_file(file_path):
    """
    Parse the given JSON file and load it as a dictionary object.

    Parameters:
    file_path (str): The path to the JSON file.

    Returns:
    dict: The parsed JSON data.
    """
    with open(file_path, 'r', encoding='utf-8') as file:
        data = json.load(file)  # Use json.load() to read the file and parse it into a dictionary
    return data

# Save the cleaned json
def save_to_json(data, filename = "../data/cleaned_data.json"):
    try:
        # Save dictionary data to JSON file
        with open(filename, 'w', encoding='utf-8') as json_file:
            json.dump(data, json_file, ensure_ascii=False, indent=4)
        print(f"Data has been successfully saved to {filename}")
    except Exception as e:
        print(f"Error saving to JSON file: {e}")

### Data cleaning

raw_data = load_json_from_file(json_file_path)
added_check_data = add_checkin_checkout_dates(raw_data)
added_city_data = assign_city_to_listings(added_check_data)
cleaned_data = clean_invalid_records(added_city_data)

save_to_json(cleaned_data)