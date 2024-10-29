import json
import matplotlib.pyplot as plt
from datetime import datetime
import matplotlib.dates as mdates

# Load data from stores.json file
with open('stores.json', 'r') as file:
    data = json.load(file)

# Extract data for the first store (Trondheim, Trondheim Torg)
store_data = data['stores'][0]['products']

# Helper function to plot stock levels
def plot_stock_levels(product_id, timestamps, levels):
    # Convert timestamp strings to datetime objects
    dates = [datetime.strptime(ts, "%Y-%m-%dT%H:%M:%S.%fZ") for ts in timestamps]

    # Plotting
    plt.figure(figsize=(10, 6))
    plt.plot(dates, levels, marker='o', linestyle='-', label=f'Product {product_id}')
    plt.xlabel('Timestamp')
    plt.ylabel('Stock Level')
    plt.title(f'Stock Levels for Product {product_id} at Trondheim Torg')
    plt.gca().xaxis.set_major_formatter(mdates.DateFormatter('%Y-%m-%d %H:%M'))
    plt.gca().xaxis.set_major_locator(mdates.HourLocator(interval=4))
    plt.xticks(rotation=45)
    plt.legend()
    plt.tight_layout()
    plt.show()

# Plot stock levels for each product in the store
for product_id, data in store_data.items():
    plot_stock_levels(product_id, data['timestamps'], data['levels'])