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