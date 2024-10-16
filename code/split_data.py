import pandas as pd

file_path = './data/updated_output_data.xlsx'
data = pd.read_excel(file_path)

one_day = data[data['Length of lease'] == 'one day']
one_week = data[data['Length of lease'] == 'one week']
one_month = data[data['Length of lease'] == 'one month']

one_day_path = './data/one_day.xlsx'
one_week_path = './data/one_week.xlsx'
one_month_path = './data/one_month.xlsx'

one_day.to_excel(one_day_path, index=False)
one_week.to_excel(one_week_path, index=False)
one_month.to_excel(one_month_path, index=False)