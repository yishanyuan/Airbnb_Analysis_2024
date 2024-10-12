from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from urllib.parse import urlencode
import time
from bs4 import BeautifulSoup
import os
import json

def search(driver, property_links, where, checkin, checkout, adults=1, children=0, infants=0):
    """
    根据给定的搜索参数，模拟 Airbnb 搜索并抓取房源链接
    """
    base_url = "https://www.airbnb.com/s/homes"
    
    # 查询参数
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

    # 构造初始搜索URL
    search_url = f"{base_url}?{urlencode(params)}"
    
    driver.get(search_url)
    time.sleep(5)  # 等待页面加载

    while True:
        # 使用 BeautifulSoup 解析当前页面
        soup = BeautifulSoup(driver.page_source, "html.parser")

        # 提取房源链接
        links = soup.find_all("a", href=True)
        for link in links:
            href = link['href']
            if "/rooms/" in href:
                full_url = f"https://www.airbnb.com{href}"
                if full_url not in property_links:
                    property_links.append(full_url)

        # 查找下一页按钮
        try:
            next_button = WebDriverWait(driver, 5).until(
                EC.presence_of_element_located((By.XPATH, "//a[@aria-label='Next']"))
            )
            next_button.click()
            time.sleep(5)  # 等待页面加载
        except Exception as e:
            print("没有更多页面可供抓取。")
            break

def save_urls(url_list, save_directory, file_name="property_links.json"):
    """
    保存 URL 列表为 JSON 文件
    """
    file_path = os.path.join(save_directory, file_name)

    # 将 URL 列表保存为 JSON 文件
    try:
        with open(file_path, 'w') as json_file:
            json.dump(url_list, json_file, indent=4)
        print(f"URL list successfully saved to {file_path}")
    except Exception as e:
        print(f"Failed to save URL list to JSON: {e}")

def load_urls(save_directory, file_name="property_links.json"):
    """
    加载保存的 URL 列表
    """
    file_path = os.path.join(save_directory, file_name)

    # 读取 JSON 文件中的 URL 列表
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