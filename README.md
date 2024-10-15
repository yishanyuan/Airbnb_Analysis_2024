# Midterm_Project_2024


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
