from selenium.common.exceptions import TimeoutException
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
import time
from bs4 import BeautifulSoup
import json
import re

def get_room_details_page(driver, room_url):
    """
    Visit the given room details page, simulate user actions, and return the BeautifulSoup object
    """
    
    try:
        driver.refresh()
        driver.get(room_url)
        time.sleep(5)  

        # Check and close the translation popup
        try:
            popup_element = WebDriverWait(driver, 5).until(
                EC.presence_of_element_located((By.XPATH, "//div[@role='dialog' and contains(@aria-label, 'Translation')]"))
            )
            close_button = popup_element.find_element(By.XPATH, ".//button[@aria-label='Close']")
            close_button.click()
            time.sleep(2)
            print("Translation popup closed.")
        except TimeoutException:     
            print("No translation popup found.")
        except Exception as e:
            print(f"Failed to find or close the translation popup: {e}")

        # Parse the content using BeautifulSoup
        soup = BeautifulSoup(driver.page_source, "html.parser")
        print(f"Loaded room details for: {room_url}")
        return soup
    except Exception as e:
        print(f"Failed to load page: {e}")
        return None
    
def extract_room_features(driver):
    """
    Extract the room's features (e.g., "City skyline view") and close the popup after extraction
    """
    
    try:
        # Wait for the "Show all amenities" button to appear and be clickable
        show_amenities_button = WebDriverWait(driver, 3).until(
            EC.element_to_be_clickable((By.XPATH, "//button[contains(text(), 'Show all')]"))
        )
        show_amenities_button.click()
        time.sleep(2)
        print("Clicked 'Show all amenities' button successfully.")
    except Exception as e:
        print(f"Failed to find or click the 'Show all amenities' button: {e}")

    try:
        # Wait for the elements describing the room features to load
        features_elements = WebDriverWait(driver, 2).until(
            EC.presence_of_all_elements_located((By.XPATH, "//div[contains(@class, 'twad414')]"))
        )
        print("Features elements located successfully.")

        # Extract and clean the text of each element
        features = []
        for element in features_elements:
            text = element.text.strip()
            if text:
                features.append(text)

        if not features:
            raise ValueError("Features list is empty after extracting text.")
        print(f"Extracted room features: {features}")

        # Simulate clicking the close button
        try:
            close_button = WebDriverWait(driver, 2).until(
                EC.element_to_be_clickable((By.XPATH, "//button[@aria-label='Close']"))
            )
            close_button.click()
            time.sleep(1)
            print("Closed the amenities popup successfully.")
        except Exception as e:
            print(f"Failed to find or click the close button: {e}")

        return features
    except Exception as e:
        print(f"Failed to extract room features: {e}")
        return []
    
def extract_price_info(driver):
    """
    Extract the complete price information, including the nightly rate, total price, cleaning fees, and service fees
    """
    
    try:
        # Wait for the page to load before getting the entire page source
        time.sleep(1)
        soup = BeautifulSoup(driver.page_source, "html.parser")

       
        prices = {}

        # Handle the first type of price label(VIP)
        price_items = soup.find_all("div", class_="_14omvfj")
        for item in price_items:
            price_name_element = item.find("div", class_="l1x1206l")
            price_value_element = item.find("span", class_="_1k4xcdh")

            if price_name_element and price_value_element:
                price_name = re.sub(r'[\d$]', '', price_name_element.text.strip()).strip()
                price_value = re.sub(r'[^\d.]', '', price_value_element.text.strip())

                if price_value:
                    prices[price_name] = float(price_value)

        # Handle the second type of price label(Normal)
        price_container_2 = soup.find("div", class_="_wgmchy")
        if price_container_2:
            price_details = price_container_2.find("div", class_="_1jo4hgw")
            
            if price_details:
                discounted_price_element = price_details.find("span", class_="_1aejdbt")
                original_price_element = price_details.find("span", class_="_11jcbg2")
                nights_element = price_details.find("span", class_="_ni9jsr")

                if discounted_price_element and nights_element:
                    discounted_price = re.sub(r'[^\d.]', '', discounted_price_element.text.strip())
                    if discounted_price:
                        prices["Price Per Night"] = float(discounted_price)

                if original_price_element:
                    original_price = re.sub(r'[^\d.]', '', original_price_element.text.strip())
                    if original_price:
                        prices["Original Price Per Night"] = float(original_price)

                if nights_element:
                    nights_match = re.search(r'\d+', nights_element.text)
                    if nights_match:
                        nights_text = re.sub(r'[\d$]', '', nights_element.text.strip()).strip()
                        nights_count = int(nights_match.group())
                        prices[nights_text] = nights_count

        print(f"Extracted prices: {prices}")
        return prices
    except Exception as e:
        print(f"Failed to extract price information: {e}")
        return {}

def extract_house_rules(driver):
    """
    Extract the house rules of the room, simulating a click on the "Show more" button
    """
    try:
        # Wait for the House Rules section to appear
        house_rules_section = WebDriverWait(driver, 2).until(
            EC.presence_of_element_located((By.XPATH, "//h3[contains(text(), 'House rules')]/ancestor::div[contains(@class, 'c1e17v3g')]"))
        )
        print("House rules section found.")

        # Try to click the "Show more" button
        try:
            show_more_button = WebDriverWait(house_rules_section, 3).until(
                EC.element_to_be_clickable((By.XPATH, ".//button[contains(., 'Show more')]"))
            )
            show_more_button.click()
            time.sleep(2)
            print("Clicked 'Show more' button successfully.")
        except Exception as e:
            print(f"Failed to find or click the 'Show more' button: {e}")


        house_rules = []
        try:
            # Extract all div elements containing house rules information
            rules_elements = WebDriverWait(driver, 2).until(
                EC.presence_of_all_elements_located((By.XPATH, "//section//div[contains(@class, 't1rc5p4c')]"))
            )

            house_rules = [element.text for element in rules_elements]
            print(f"Extracted house rules: {house_rules}")
        except Exception as e:
            print(f"Failed to extract house rules information: {e}")

        # Simulate clicking the close button
        try:
            close_button = WebDriverWait(driver, 2).until(
                EC.element_to_be_clickable((By.XPATH, "//button[@aria-label='Close']"))
            )
            close_button.click()
            time.sleep(1) 
            print("Closed the house rule popup successfully.")
        except Exception as e:
            print(f"Failed to find or click the close button: {e}")

        return house_rules
    except Exception as e:
        print(f"Failed to find the House Rules section: {e}")
        return []
    
def save_to_json(data, filename = "rooms_details.json"):
    """
    Save the dictionary data into a JSON file
    """
    
    try:
        with open(filename, 'w', encoding='utf-8') as json_file:
            json.dump(data, json_file, ensure_ascii=False, indent=4)
        print(f"Data successfully saved to {filename}")
    except Exception as e:
        print(f"Error saving to JSON file: {e}")
