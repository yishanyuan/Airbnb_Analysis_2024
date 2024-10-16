import pandas as pd
from openpyxl import load_workbook

# 定义数据文件相对路径
input_file_path = './data/variables_output.csv'
output_file_path = './data/updated_output_data.xlsx'

# 读取CSV文件，使用相对路径
data = pd.read_csv(input_file_path)

# 增加'Length of lease'列，并设置为空值
data['Length of lease'] = ''

# 确保日期格式与数据一致 'YYYY-MM-DD'
data['Check Out'] = data['Check Out'].astype(str)

# 更新'Length of lease'列，根据你提供的日期条件
data.loc[data['Check Out'] == '2024-11-02', 'Length of lease'] = 'one day'
data.loc[data['Check Out'].isin(['2024-11-07', '2024-11-06', '2024-11-09', '2024-11-08']), 'Length of lease'] = 'one week'
data.loc[data['Check Out'].isin(['2024-11-30', '2024-12-01', '2024-12-03', '2024-12-04', '2024-12-05', '2024-12-06']), 'Length of lease'] = 'one month'

# 删除 'Cleaning Fee' 和 'Airbnb Service Fee' 列
data = data.drop(columns=['Cleaning Fee', 'Airbnb Service Fee'])

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