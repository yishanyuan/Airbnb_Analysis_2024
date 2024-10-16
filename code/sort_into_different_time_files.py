import pandas as pd
from openpyxl import load_workbook

input_file_path = './data/variables_output.csv'
output_file_path = './data/updated_output_data.xlsx'

data = pd.read_csv(input_file_path)

data['Length of lease'] = ''

data['Check Out'] = data['Check Out'].astype(str)

data.loc[data['Check Out'] == '2024-11-02', 'Length of lease'] = 'one day'
data.loc[data['Check Out'].isin(['2024-11-07', '2024-11-06', '2024-11-09', '2024-11-08']), 'Length of lease'] = 'one week'
data.loc[data['Check Out'].isin(['2024-11-30', '2024-12-01', '2024-12-03', '2024-12-04', '2024-12-05', '2024-12-06']), 'Length of lease'] = 'one month'

data = data.drop(columns=['Cleaning Fee', 'Airbnb Service Fee'])

data.loc[data['Length of lease'] == 'one month', 'Price Per Night'] = data.loc[data['Length of lease'] == 'one month', 'Price Per Night'] / 30

data.to_excel(output_file_path, index=False)

wb = load_workbook(output_file_path)
ws = wb.active

ws.column_dimensions['C'].width = 20
ws.column_dimensions['D'].width = 20

wb.save(output_file_path)

print("updated")