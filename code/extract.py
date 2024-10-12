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
    访问给定的房间详情链接，模拟人类操作并返回 BeautifulSoup 对象
    """
    try:
        driver.refresh()
        driver.get(room_url)
        time.sleep(5)  # 等待页面加载

        # 检查并关闭翻译弹窗
        try:
            # 查找翻译弹窗并点击关闭按钮
            popup_element = WebDriverWait(driver, 5).until(
                EC.presence_of_element_located((By.XPATH, "//div[@role='dialog' and contains(@aria-label, 'Translation')]"))
            )
            close_button = popup_element.find_element(By.XPATH, ".//button[@aria-label='Close']")
            close_button.click()
            time.sleep(2)  # 等待弹窗关闭
            print("Translation popup closed.")
        except TimeoutException:
            # 如果在规定时间内没有找到翻译弹窗，这是正常的，不需要视为错误
            print("No translation popup found.")
        except Exception as e:
            print(f"未能找到或关闭翻译弹窗: {e}")

        # 用 BeautifulSoup 解析内容
        soup = BeautifulSoup(driver.page_source, "html.parser")
        print(f"Loaded room details for: {room_url}")
        return soup
    except Exception as e:
        print(f"请求失败: {e}")
        return None
    
def extract_room_features(driver):
    """
    获取房间的特征描述（如“City skyline view”），并在提取完成后关闭弹窗
    """
    try:
        # 等待“Show all amenities”按钮出现并可点击
        show_amenities_button = WebDriverWait(driver, 3).until(
            EC.element_to_be_clickable((By.XPATH, "//button[contains(text(), 'Show all')]"))
        )
        show_amenities_button.click()
        time.sleep(2)  # 等待弹出窗口加载
        print("Clicked 'Show all amenities' button successfully.")
    except Exception as e:
        print(f"未能找到或点击 'Show all amenities' 按钮: {e}")

    try:
        # 等待描述房间特征的元素加载
        features_elements = WebDriverWait(driver, 2).until(
            EC.presence_of_all_elements_located((By.XPATH, "//div[contains(@class, 'twad414')]"))
        )
        print("Features elements located successfully.")

        # 提取并清理每个 element 的文本
        features = []
        for element in features_elements:
            text = element.text.strip()  # 去除前后的空白字符
            if text:  # 如果文本非空
                features.append(text)

        if not features:
            raise ValueError("Features list is empty after extracting text.")
        print(f"Extracted room features: {features}")

        # 模拟点击关闭按钮
        try:
            close_button = WebDriverWait(driver, 2).until(
                EC.element_to_be_clickable((By.XPATH, "//button[@aria-label='Close']"))
            )
            close_button.click()
            time.sleep(1)  # 等待弹窗关闭
            print("Closed the amenities popup successfully.")
        except Exception as e:
            print(f"未能找到或点击关闭按钮: {e}")

        return features
    except Exception as e:
        print(f"未能提取房间特征信息: {e}")
        return []
    
def extract_price_info(driver):
    """
    获取房间的完整价格信息，包括单价、总价、清洁费、服务费等
    """
    try:
        # 等待页面加载后获取整个页面源代码
        time.sleep(1)  # 可以根据需要调整，确保页面加载完成
        soup = BeautifulSoup(driver.page_source, "html.parser")

        # 存储所有价格信息的字典
        prices = {}

        # 处理第一种价格标签类型
        price_items = soup.find_all("div", class_="_14omvfj")
        for item in price_items:
            price_name_element = item.find("div", class_="l1x1206l")
            price_value_element = item.find("span", class_="_1k4xcdh")

            if price_name_element and price_value_element:
                # 使用正则表达式清理键的文本
                price_name = re.sub(r'[\d$]', '', price_name_element.text.strip()).strip()
                price_value = re.sub(r'[^\d.]', '', price_value_element.text.strip())

                # 确保价格值可以正确转换为浮点数
                if price_value:
                    prices[price_name] = float(price_value)

        # 处理第二种价格标签类型
        price_container_2 = soup.find("div", class_="_wgmchy")
        if price_container_2:
            # 提取单价和原价信息
            price_details = price_container_2.find("div", class_="_1jo4hgw")
            if price_details:
                # 提取折扣后的价格和原价
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

                # 提取夜数信息
                if nights_element:
                    nights_match = re.search(r'\d+', nights_element.text)
                    if nights_match:
                        nights_text = re.sub(r'[\d$]', '', nights_element.text.strip()).strip()
                        nights_count = int(nights_match.group())
                        prices[nights_text] = nights_count

        print(f"Extracted prices: {prices}")
        return prices
    except Exception as e:
        print(f"未能提取价格信息: {e}")
        return {}

def extract_house_rules(driver):
    """
    获取房间的 House Rules 信息，模拟点击 "Show more" 按钮并提取信息
    """
    try:
        # 等待 House Rules 部分出现
        house_rules_section = WebDriverWait(driver, 2).until(
            EC.presence_of_element_located((By.XPATH, "//h3[contains(text(), 'House rules')]/ancestor::div[contains(@class, 'c1e17v3g')]"))
        )
        print("House rules section found.")

        # 尝试点击 "Show more" 按钮
        try:
            # 使用更广泛的定位器查找 Show more 按钮
            show_more_button = WebDriverWait(house_rules_section, 3).until(
                EC.element_to_be_clickable((By.XPATH, ".//button[contains(., 'Show more')]"))
            )
            show_more_button.click()
            time.sleep(2)  # 等待弹窗加载
            print("Clicked 'Show more' button successfully.")
        except Exception as e:
            print(f"未能找到或点击 'Show more' 按钮: {e}")

        # 提取 house rules 信息
        house_rules = []
        try:
            # 提取所有包含 House Rules 信息的 div 元素
            rules_elements = WebDriverWait(driver, 2).until(
                EC.presence_of_all_elements_located((By.XPATH, "//section//div[contains(@class, 't1rc5p4c')]"))
            )

            house_rules = [element.text for element in rules_elements]
            print(f"Extracted house rules: {house_rules}")
        except Exception as e:
            print(f"未能提取 House Rules 信息: {e}")

        # 模拟点击关闭按钮
        try:
            close_button = WebDriverWait(driver, 2).until(
                EC.element_to_be_clickable((By.XPATH, "//button[@aria-label='Close']"))
            )
            close_button.click()
            time.sleep(1)  # 等待弹窗关闭
            print("Closed the house rule popup successfully.")
        except Exception as e:
            print(f"未能找到或点击关闭按钮: {e}")

        return house_rules
    except Exception as e:
        print(f"未能找到 House Rules 部分: {e}")
        return []
    
def save_to_json(data, filename = "rooms_details.json"):
    try:
        # 将字典数据保存到 JSON 文件
        with open(filename, 'w', encoding='utf-8') as json_file:
            json.dump(data, json_file, ensure_ascii=False, indent=4)
        print(f"数据已成功保存到 {filename}")
    except Exception as e:
        print(f"保存到 JSON 文件时出错: {e}")