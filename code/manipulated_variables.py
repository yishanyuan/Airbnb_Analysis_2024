import pandas as pd
import os

# Define the base directory for your project (moving up one level to the project root directory)
base_dir = os.path.dirname(os.path.dirname(__file__))  # 上一级目录

# Define relative paths for input CSV and output CSV (located in 'data' folder)
data_folder_path = os.path.join(base_dir, 'data')
csv_file_path = os.path.join(data_folder_path, 'output_data.csv')  
updated_csv_file_path = os.path.join(data_folder_path, 'variables_output_data.csv')  # 生成后的CSV文件名

# Load the CSV file into a DataFrame
df = pd.read_csv(csv_file_path)

# Define the feature columns to be added
df['Smoking allowed'] = df['Features'].apply(lambda x: 'True' if 'Smoking allowed' in x else 'False')
df['Pets allowed'] = df['Features'].apply(lambda x: 'True' if 'Pets allowed' in x else 'False')
df['Free parking'] = df['Features'].apply(lambda x: 'True' if 'Free parking' in x else 'False')

# Save the updated DataFrame back to a CSV
df.to_csv(updated_csv_file_path, index=False)

print(f"CSV file updated and saved at {updated_csv_file_path}")