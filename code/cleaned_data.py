import re
import json

json_file_path = "../data/file.json"

def load_json_from_file(file_path):
    """
    解析给定的 JSON 文件并将其加载为字典对象。
    
    参数:
    file_path (str): JSON 文件的路径。
    
    返回:
    dict: 解析后的 JSON 数据。
    """
    with open(file_path, 'r', encoding='UTF-8') as file:
        data = json.load(file)  # 使用 json.load() 读取文件并解析为字典
    return data

def add_checkin_checkout_dates(data):
    """
    从 JSON 对象的 URL 键中提取 check_in 和 check_out 日期，并将它们添加到每个房源的详细信息中。

    参数:
    data (dict): 原始 JSON 数据，其中 URL 是每个键。

    返回:
    dict: 更新后的 JSON 数据，带有 check_in 和 check_out 日期。
    """
    # 正则表达式用于匹配 check_in 和 check_out 日期
    date_pattern = r'check_in=(\d{4}-\d{2}-\d{2})&check_out=(\d{4}-\d{2}-\d{2})'
    
    # 新字典，用于存储更新后的数据
    updated_data = {}
    
    # 遍历所有 URL
    for key, value in data.items():
        match = re.search(date_pattern, key)
        if match:
            # 提取日期
            check_in, check_out = match.groups()
            # 将新日期添加到 value 字典中
            value['check_in'] = check_in
            value['check_out'] = check_out
        # 将更新后的 value 重新添加到 updated_data 中
        updated_data[key] = value
    
    return updated_data

# 保存清洗完的 json
def save_to_json(data, filename = "cleaned_data.json"):
    try:
        # 将字典数据保存到 JSON 文件
        with open(filename, 'w', encoding='utf-8') as json_file:
            json.dump(data, json_file, ensure_ascii=False, indent=4)
        print(f"数据已成功保存到 {filename}")
    except Exception as e:
        print(f"保存到 JSON 文件时出错: {e}")

raw_data = load_json_from_file(json_file_path)
added_check_data = add_checkin_checkout_dates(raw_data)
save_to_json(added_check_data)