import pandas as pd
from openpyxl import load_workbook

# 定义数据文件相对路径（相对于 code 文件夹）
input_file_path = "./data/variables_output.csv"
output_file_path = './data/updated_output_data.xlsx'

# 读取CSV文件，使用相对路径
data = pd.read_csv(input_file_path)

# 增加'Length of lease'列，并设置为空值
data['Length of lease'] = ''

# 更新'Length of lease'列，根据你提供的日期条件
data.loc[data['Check Out'] == '2024/11/2', 'Length of lease'] = 'one day'
data.loc[data['Check Out'].isin(['2024/11/7', '2024/11/6', '2024/11/9', '2024/11/8']), 'Length of lease'] = 'one week'
data.loc[data['Check Out'].isin(['2024/11/30', '2024/12/1', '2024/12/3', '2024/12/4', '2024/12/5', '2024/12/6']), 'Length of lease'] = 'one month'

# 保存为Excel文件，使用相对路径
data.to_excel(output_file_path, index=False)

# 使用openpyxl调整Excel中的C列和D列宽度
wb = load_workbook(output_file_path)
ws = wb.active

# 将C列和D列变宽
ws.column_dimensions['C'].width = 20
ws.column_dimensions['D'].width = 20

# 保存调整后的Excel文件
wb.save(output_file_path)

print("文件已更新并保存")