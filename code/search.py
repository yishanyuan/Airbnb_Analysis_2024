from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from urllib.parse import urlencode
import time
from bs4 import BeautifulSoup
import os
import json

def search(driver, property_links, where, checkin, checkout, adults=1, children=0, infants=0):

    # Simulate an Airbnb search and scrape property links based on the given search parameters
    base_url = "https://www.airbnb.com/s/homes"
    
    params = {
        "query": where,
        "checkin": checkin,
        "checkout": checkout,
        "adults": adults,
        "children": children,
        "infants": infants,
        "tab_id": "home_tab",
        "search_type": "autocomplete_click",
        "source": "structured_search_input_header",
    }

    search_url = f"{base_url}?{urlencode(params)}"
    
    driver.get(search_url)
    time.sleep(5)

    while True:
        # Parse the current page using BeautifulSoup
        soup = BeautifulSoup(driver.page_source, "html.parser")

        # Extract property links
        links = soup.find_all("a", href=True)
        for link in links:
            href = link['href']
            if "/rooms/" in href:
                full_url = f"https://www.airbnb.com{href}"
                if full_url not in property_links:
                    property_links.append(full_url)

        # Find the "Next" button
        try:
            next_button = WebDriverWait(driver, 5).until(
                EC.presence_of_element_located((By.XPATH, "//a[@aria-label='Next']"))
            )
            next_button.click()
            time.sleep(5)
        except Exception as e:
            print("No more pages available for scraping.")
            break

def save_urls(url_list, save_directory, file_name="property_links.json"):
    
   # Save the URL list as a JSON file
    file_path = os.path.join(save_directory, file_name)

    try:
        with open(file_path, 'w') as json_file:
            json.dump(url_list, json_file, indent=4)
        print(f"URL list successfully saved to {file_path}")
    except Exception as e:
        print(f"Failed to save URL list to JSON: {e}")

def load_urls(save_directory, file_name="property_links.json"):
    
    # Load the saved URL list
    file_path = os.path.join(save_directory, file_name)

    try:
        if os.path.exists(file_path):
            with open(file_path, 'r') as json_file:
                url_list = json.load(json_file)
                print(f"URL list successfully loaded from {file_path}")
                return url_list
        else:
            print(f"No URL file found at {file_path}")
            return []
    except Exception as e:
        print(f"Failed to load URL list from JSON: {e}")
        return []
