from selenium import webdriver
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.chrome.options import Options
from webdriver_manager.chrome import ChromeDriverManager
import os

from search import search
from search import save_urls
from search import load_urls

from extract import get_room_details_page
from extract import extract_room_features
from extract import extract_price_info
from extract import extract_house_rules
from extract import save_to_json

def open():
    # Set headless browser options
    optionsSettings = Options()
    optionsSettings.add_argument("--headless=new")
    optionsSettings.add_argument("--disable-gpu")
    optionsSettings.add_argument("--window-size=1920,1080")
    optionsSettings.add_argument("--no-sandbox")
    optionsSettings.add_argument("--disable-dev-shm-usage")

    # Set up Selenium WebDriver, using WebDriver Manager to automatically download ChromeDriver
    service = Service(ChromeDriverManager().install())
    return webdriver.Chrome(options=optionsSettings, service=service)
    

def close(driver):
    # Close Selenium WebDriver
    driver.quit()

save_directory = os.getcwd()
if not os.path.exists(save_directory):
    os.makedirs(save_directory)
print(f"Save directory set to: {save_directory}")





# Execute the logical flow
driver = open()


# Parameters
cities = ["Austin, TX", "New York City, NY", "Chicago, IL", "Los Angeles, CA"]
checkin = "2024-11-01"
checkouts = ["2024-11-02", "2024-11-07", "2024-11-30"]
adults = 1


# Search properties links & save them
property_links = []
search(driver, property_links, where checkin, checkout)

 for city in cities:
     for checkout in checkouts:
         e = search(driver, property_links, city, checkin, checkout)
         property_links.append(e)



save_urls(property_links, save_directory)


# Extract rooms details
property_links = load_urls(save_directory)

rooms_details = {}

for i in range(len(property_links)):
    room_url = property_links[i]
    get_room_details_page(driver, room_url)
    features = extract_room_features(driver)
    prices = extract_price_info(driver)
    house_rules = extract_house_rules(driver)
    rooms_details[room_url] = {'features': features, 'prices': prices, 'house_rules': house_rules}

save_to_json(rooms_details, "file.json")

close(driver)
