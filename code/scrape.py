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
    # 设置无头浏览器选项
    optionsSettings = Options()
    optionsSettings.add_argument("--headless=new")  # 使用新的 headless 模式
    optionsSettings.add_argument("--disable-gpu")
    optionsSettings.add_argument("--window-size=1920,1080")
    optionsSettings.add_argument("--no-sandbox")  # 尝试避免一些 sandbox 限制
    optionsSettings.add_argument("--disable-dev-shm-usage")  # 避免 /dev/shm 空间不足

    # 设置 Selenium WebDriver，使用 WebDriver Manager 自动下载 ChromeDriver
    service = Service(ChromeDriverManager().install())
    return webdriver.Chrome(options=optionsSettings, service=service) # No windows
    # return webdriver.Chrome(service=service) # Has windows

def close(driver):
    """
    关闭 Selenium WebDriver
    """
    driver.quit()

save_directory = os.getcwd()
if not os.path.exists(save_directory):
    os.makedirs(save_directory)
print(f"Save directory set to: {save_directory}")









# 执行邏輯流程

driver = open()

"""
Parameters
"""
cities = ["Austin, TX", "New York City, NY", "Chicago, IL", "Los Angeles, CA"]
checkin = "2024-11-01"
checkouts = ["2024-11-02", "2024-11-07", "2024-11-30"]
adults = 1

# where = "Austin, TX"
# checkin = "2024-10-27"
# checkout = "2024-11-02"
# adults = 1

"""
Search properties links & save them
"""
property_links = []
#search(driver, property_links, where checkin, checkout)

# for city in cities:
#     for checkout in checkouts:
#         e = search(driver, property_links, city, checkin, checkout)
#         property_links.append(e)


# #儲存（要再打）
# save_urls(property_links, save_directory)

"""
Extract rooms details
"""
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

# 关闭浏览器
close(driver)