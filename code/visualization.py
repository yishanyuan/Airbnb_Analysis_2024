import matplotlib.pyplot as plt
import seaborn as sns
import pandas as pd

def plot_price_distribution(data, bins=20, kde=True):
    """
    
    """
    
    one_day_data = data[data['Length of lease'] == 'one day']

    
    plt.figure(figsize=(10, 6))
    sns.histplot(one_day_data['Price Per Night'], bins=bins, kde=kde, color='green')
    plt.title('Price Distribution of One-Day Airbnb Listings')
    plt.xlabel('Price Per Night ($)')
    plt.ylabel('Frequency')
    plt.grid(True)
    plt.tight_layout()
    

def plot_city_comparison_boxplot(data, selected_cities):
    """
    
    """
    
    one_day_data = data[data['Length of lease'] == 'one day']
    df_filtered = one_day_data[one_day_data['City'].isin(selected_cities)]

    
    plt.figure(figsize=(10, 6))
    sns.boxplot(x='City', y='Price Per Night', data=df_filtered)
    plt.title('Comparison of One-Day Airbnb Prices in Selected Cities')
    plt.xlabel('City')
    plt.ylabel('Price Per Night ($)')
    plt.grid(True)
    plt.xticks(rotation=45)  
    plt.tight_layout()

def plot_pet_combined_price_distributions(one_day_file, one_week_file, one_month_file, output_file):
    """
    
    """
    
    fig, axes = plt.subplots(1, 3, figsize=(18, 6)) 

    
    data_one_month = pd.read_excel(one_month_file)
    sns.histplot(data=data_one_month, x='Price Per Night', hue='Pets allowed', multiple='stack', bins=20, palette='Set2', ax=axes[0])
    axes[0].set_title('One Month Price Distribution')
    axes[0].set_xlabel('One Month Price ($)')
    axes[0].set_ylabel('Count')

   
    data_one_week = pd.read_excel(one_week_file)
    sns.histplot(data=data_one_week, x='Price Per Night', hue='Pets allowed', multiple='stack', bins=20, palette='Set2', ax=axes[1])
    axes[1].set_title('One Week Price Distribution')
    axes[1].set_xlabel('One Week Price ($)')
    axes[1].set_ylabel('')

    
    data_one_day = pd.read_excel(one_day_file)
    sns.histplot(data=data_one_day, x='Price Per Night', hue='Pets allowed', multiple='stack', bins=20, palette='Set2', ax=axes[2])
    axes[2].set_title('One Day Price Distribution')
    axes[2].set_xlabel('One Day Price ($)')
    axes[2].set_ylabel('')

   
    plt.tight_layout()
    plt.savefig(output_file, format='png')

def plot_smoking_allowed_boxplots(one_month_file, one_week_file, one_day_file, output_file):
    fig, axes = plt.subplots(1, 3, figsize=(18, 6)) 

    
    data_one_month = pd.read_excel(one_month_file)
    sns.boxplot(x='Smoking allowed', y='Price Per Night', data=data_one_month, palette='Set2', ax=axes[0])
    axes[0].set_title('One Month Price Distribution by Smoking Allowed')
    axes[0].set_xlabel('Smoking Allowed')
    axes[0].set_ylabel('One Month Price ($)')

    
    data_one_week = pd.read_excel(one_week_file)
    sns.boxplot(x='Smoking allowed', y='Price Per Night', data=data_one_week, palette='Set2', ax=axes[1])
    axes[1].set_title('One Week Price Distribution by Smoking Allowed')
    axes[1].set_xlabel('Smoking Allowed')
    axes[1].set_ylabel('One Week Price ($)')

   
    data_one_day = pd.read_excel(one_day_file)
    sns.boxplot(x='Smoking allowed', y='Price Per Night', data=data_one_day, palette='Set2', ax=axes[2])
    axes[2].set_title('One Day Price Distribution by Smoking Allowed')
    axes[2].set_xlabel('Smoking Allowed')
    axes[2].set_ylabel('One Day Price ($)')

    plt.tight_layout()
    plt.savefig(output_file, format='png')
    

def plot_free_parking_barplots(one_month_file, one_week_file, one_day_file, output_file):
    """
    
    """
    
    fig, axes = plt.subplots(1, 3, figsize=(18, 6))  

    
    data_one_month = pd.read_excel(one_month_file)
    sns.barplot(x='Free parking', y='Price Per Night', data=data_one_month, palette='Set2', ax=axes[0])
    axes[0].set_title('One Month Average Price by Free Parking')
    axes[0].set_xlabel('Free Parking')
    axes[0].set_ylabel('One Month Price ($)')

   
    data_one_week = pd.read_excel(one_week_file)
    sns.barplot(x='Free parking', y='Price Per Night', data=data_one_week, palette='Set2', ax=axes[1])
    axes[1].set_title('One Week Average Price by Free Parking')
    axes[1].set_xlabel('Free Parking')
    axes[1].set_ylabel('One Week Price ($)')

    
    data_one_day = pd.read_excel(one_day_file)
    sns.barplot(x='Free parking', y='Price Per Night', data=data_one_day, palette='Set2', ax=axes[2])
    axes[2].set_title('One Day Average Price by Free Parking')
    axes[2].set_xlabel('Free Parking')
    axes[2].set_ylabel('One Day Price ($)')

 
    plt.tight_layout()
    plt.savefig(output_file, format='png')
  


input_path = "./data/"
output_path = "./artifacts/"

file_path = input_path + 'updated_output_data.xlsx'
data = pd.read_excel(file_path)
selected_cities = ['Austin, TX', 'New York City, NY', 'Chicago, IL', 'Los Angeles, CA']

plot_price_distribution(data)

plot_city_comparison_boxplot(data, selected_cities)



plot_pet_combined_price_distributions(
    one_day_file=input_path +  'one_day_output_data.xlsx',
    one_week_file=input_path +  'one_week_output_data.xlsx',
    one_month_file=input_path + 'one_month_output_data.xlsx',
    output_file=output_path +  'combined_price_distributions.png'
)



plot_free_parking_barplots(
    one_month_file= input_path + 'one_month_output_data.xlsx',
    one_week_file= input_path +'one_week_output_data.xlsx',
    one_day_file= input_path + 'one_day_output_data.xlsx',
    output_file= output_path +  'combined_barplot_free_parking_price_output.png'
)

plot_smoking_allowed_boxplots(
    one_month_file= input_path +'one_month_output_data.xlsx',
    one_week_file= input_path +  'one_week_output_data.xlsx',
    one_day_file= input_path + 'one_day_output_data.xlsx',
    output_file= output_path +'combined_boxplot_smoking_allowed_price.png'
)

   
