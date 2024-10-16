# Midterm_Project_2024

# Installation



# Quick Start


# Search Data
Automating the process of searching for Airbnb listings based on specified search parameters, extracting property links, and saving/loading these links for future use.

**Functions Used:** <br>
`search`: Simulate an Airbnb search with specific parameters (location, check-in, check-out dates, and guest details) and extracts property links from the results.<br>
`save_urls`: Save the extracted property links to a JSON file.<br>
`load_urls`: Load saved property links from a JSON file for future processing.<br>

**Processing Logic:**
The program constructs a search URL based on user input (location, check-in, check-out, etc.) and uses `Selenium` to navigate to the Airbnb results page. The HTML content of the page is parsed with `BeautifulSoup` to extract property links that contain "/rooms/". The process is repeated for all available pages by clicking the "Next" button until no more results are found. Extracted links are saved in a JSON file and can be loaded later for further use.

# Scrape Data
Automating the process of searching Airbnb property listings, extracting room details (features, prices, house rules), and saving this data into a JSON file.

**Functions Used:** <br>
`open`: Initialize the headless browser using `Selenium` WebDriver with customized options.<br>
`close`: Close the `Selenium` WebDriver once all operations are completed.<br>
`search`: Search for property links based on specified parameters (location, check-in, check-out).<br>
`save_urls`: Save the collected property links into a JSON file.<br>
`load_urls`: Load previously saved property links from a JSON file.<br>
`get_room_details_page`: Load and parse the room details page using `BeautifulSoup`.<br>
`extract_room_features`, `extract_price_info`, `extract_house_rules`: Extract room features, pricing details, and house rules respectively from each property page.<br>
`save_to_json`: Save the extracted room details into a JSON file.<br>

**Processing Logic:**
The program starts by opening a headless browser using `Selenium` WebDriver. It performs a search for property listings based on specified cities and check-in/check-out dates. Property links are extracted, and they can be saved to or loaded from a JSON file. For each property link, the page is loaded, and details such as room features, prices, and house rules are extracted. The extracted data is stored in a dictionary and saved into a JSON file for further use. After completing the extraction process, the browser is closed.


# Extract Data
Extracting detailed information about Airbnb properties (room features, prices, and house rules) from property URLs and saving this information into a JSON file.

**Functions Used:** <br>
`get_room_details_page`: Load and parse the room details page using `BeautifulSoup` after interacting with the webpage (e.g., closing popups).<br>
`extract_room_features`: Extract room features by clicking the "Show all amenities" button and parsing the content.<br>
`extract_price_info`: Extract pricing information including nightly rates, cleaning fees, and other costs from the room details page.<br>
`extract_house_rules`: Extract the house rules of a room by clicking the "Show more" button and parsing the content.<br>
`save_to_json`: Save the extracted room details into a JSON file for further use.<br>

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

## Data Processing and Price Adjustment Script (sort_into_different_time_files.py and split_data.py) ##

**Description**

This script updates the Length of lease based on Check In and Check Out dates and adjusts prices for records with a length of lease as one week and one month. It also splits the data into three separate files based on the length of lease: one day, one week, and one month. The processed data is saved as Excel files.

**Workflow**

The workflow includes reading the input CSV file, updating the Length of lease based on Check In and Check Out dates, deleting unnecessary columns like Cleaning Fee and Airbnb Service Fee, splitting the data into three files based on the Length of lease, and saving the processed data as Excel files while adjusting the column widths for date columns.

# Visualization And Analysis #

## Visualization ##

This part generates a variety of visualizations for analyzing Airbnb prices based on different factors such as city, free parking availability, pet allowance, and smoking policies. It uses Python libraries, including matplotlib, seaborn, and pandas, to create histograms, bar plots, and boxplots from data stored in Excel files .Each of these functions reads data from Excel files, processes it for the respective analysis (e.g., comparing cities, or analyzing policy effects), and generates visualizations, which are saved to a specified output location.

**Functions Used:**
`plot_price_distribution`: Generates a histogram showing one-day Airbnb price distribution.
`plot_city_comparison_boxplot`: Creates a boxplot comparing one-day prices across selected cities.
`plot_pet_combined_price_distributions` Visualizes price distributions for one-day, one-week, and one-month stays based on pet allowance.
`plot_smoking_allowed_boxplots`: Plots boxplots to compare prices for smoking and non-smoking listings.
`plot_free_parking_barplots`: Compares average prices for listings with and without free parking for different lease durations.
'`output_path = "./artifacts/"`: This specifies that the generated visualizations (PNG files) will be saved in a folder named artifacts, which is also located in the current working directory.


##  Analysis ##
**General Price Distribution**
![](./artiacts/price_distribution.png)
The histogram shows the price distribution of one-day Airbnb listings, with the x-axis representing the price per night and the y-axis showing the frequency of listings at each price point. The distribution is right-skewed, with most one-day Airbnb listings priced between $100–$150. Higher-priced listings above $200 are rare, indicating that the majority of listings are affordable, while luxury options are limited. The skew suggests that more affordable listings dominate the market, with only a few high-end accommodations available.

** City Comparison**
![](./artiacts/city_comparison.png)
The boxplot compares one-day Airbnb prices across four cities: Austin, New York City, Chicago, and Los Angeles. Austin has the highest median price (~$200), while New York City has a broader range with many lower-priced options but also several high-end outliers. Chicago and Los Angeles show more consistent pricing with fewer extreme values. Overall, Austin's prices vary widely, New York City has significant variation, and both Chicago and Los Angeles have more stable pricing with less variation in outliers.

** The effect of free parking**
[](./artiacts/combined_barplot_free_parking_price_output)
For one-month stays, prices are similar regardless of free parking. For one-day stays, listings with free parking are cheaper. Free parking shows minimal impact on one-week prices but slightly lowers prices for short-term stays. Location could indeed be a key reason for the price differences. In urban areas where parking is scarce, listings without free parking may be in more desirable or central locations, which can drive up their price. Conversely, listings with free parking might be located in less central areas where parking is easier to offer, leading to lower prices for short-term stays. For one-month rentals, location might play less of a role in price differences, as long-term renters may prioritize other factors over parking, such as proximity to work or public transport.

** The effect of pet allowed**
[](./artiacts/combined_price_distributions)
The graphs show price distributions for one-month, one-week, and one-day Airbnb listings, separated by whether pets are allowed or not.  In the One-Month Price Distribution (left), listings that allow pets (orange) are generally priced higher than those that do not, especially in the lower price ranges (up to $100). This suggests that pet-friendly long-term rentals may command a premium. In the One-Week Price Distribution (middle), a similar trend is observed, with pet-friendly listings taking a larger share in the higher price ranges compared to non-pet listings, though the difference is less pronounced than for one-month stays. For the One-Day Price Distribution (right), pet-friendly listings are more spread across various price ranges but still maintain a noticeable presence in the lower price brackets. The overall effect of allowing pets is less significant for one-day stays compared to longer-term rentals. Possible reasons for these differences include higher demand for pet-friendly listings, as renters with pets may be willing to pay more for accommodations that meet their needs, especially for long stays. Additionally, added costs for hosts associated with allowing pets, such as maintenance and cleaning, could lead to higher pricing, particularly for longer rental periods.

** The effect of smoking allowed**
[](./artiacts/combined_boxplot_smoking_allowed_price)
The boxplots show price distributions for one-month, one-week, and one-day Airbnb listings, comparing those that allow smoking versus those that do not. Listings that do not allow smoking tend to have higher prices and a wider price range, especially for one-month and one-week stays. This may be due to higher demand for non-smoking accommodations, particularly in family-friendly or urban areas, where smoking is less accepted. Non-smoking listings likely attract a broader market and are perceived as cleaner or more desirable, allowing hosts to charge a premium. Smoking-allowed listings, on the other hand, cater to a more niche audience, which could explain their lower prices and narrower price range, particularly for longer stays. For one-day stays, the price difference is less significant.
