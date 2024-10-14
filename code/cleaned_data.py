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
save_to_json(raw_data)