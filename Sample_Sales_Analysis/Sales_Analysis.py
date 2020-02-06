import pandas as pd
import matplotlib.pyplot as plt
import numpy as np
import os
from itertools import combinations
from collections import Counter

# Merge 12 months of data together
# Remove empty rows of NaN
files = [file for file in os.listdir('./Sample_Sales_Data/2019')]    
all_sales = pd.DataFrame()
for file in files:
    df = pd.read_csv('./Sample_Sales_Data/2019/{}'.format(file))
    df.dropna(how='all', inplace=True)
    all_sales = pd.concat([all_sales, df])

# Original Data contained some rows with the Header info, so those need to be removed as well
all_sales = all_sales[all_sales['Product'] != 'Product']
all_sales.reset_index(inplace=True)

# Make all data correct data type
all_sales['Quantity Ordered'] = pd.to_numeric(all_sales['Quantity Ordered'])
all_sales['Price Each'] = pd.to_numeric(all_sales['Price Each'])
all_sales['Order Date'] = pd.to_datetime(all_sales['Order Date'])

# Add Month and Hour Columns
all_sales['Month'] = all_sales['Order Date'].dt.month
all_sales['Hour'] = all_sales['Order Date'].dt.hour

# Create City (State) and ZIP columns, Remove Purchase Address column
all_sales['City'] = all_sales['Purchase Address'].str.split(',', expand=True)[1] + ', ' + all_sales['Purchase Address'].str.split(',', expand=True)[2].str.split(' ', expand=True)[1]
all_sales['ZIP'] = all_sales['Purchase Address'].str.split(',', expand=True)[2].str.split(' ', expand=True)[2]
all_sales.drop(columns='Purchase Address', inplace=True)

# Calculate Revenue
# Find Best Month
# Find Best City
# Find Best Hour
all_sales['Revenue'] = all_sales['Quantity Ordered'] * all_sales['Price Each']
monthly_revenue = all_sales.groupby('Month').sum()
city_revenue = all_sales.groupby('City').sum().sort_values(by=['Revenue'], ascending=False)
hourly_orders = all_sales.groupby('Hour').count()

# Find Items Commonly Bought Together
# Create list of top ten most frequently bought together items
item_pairs = all_sales[all_sales['Order ID'].duplicated(keep=False)]
item_pairs['Grouped'] = item_pairs.groupby('Order ID')['Product'].transform(lambda x: ','.join(x))
item_pairs = item_pairs[['Order ID', 'Grouped']].drop_duplicates()

count = Counter()
for row in item_pairs['Grouped']:
    row_list = row.split(',')
    count.update(Counter(combinations(row_list, 2)))

top_ten_pairs = []
for key, value in count.most_common(10):
    top_ten_pairs.append([key, value])

# Find Most Ordered Product
# Find Highest Revenue Product
items_sold = all_sales.groupby('Product').sum().sort_values(by=['Quantity Ordered'], ascending=False)
items_revenue = items_sold.sort_values(by=['Revenue'], ascending=False)

# Plot Results
months = range(1,13)
cities = [city for city in city_revenue.index]
hours = [hour for hour, df in all_sales.groupby('Hour')]
items_by_quant = [item for item in items_sold.index]
items_by_rev = [item for item in items_revenue.index]
fig = plt.figure(figsize=(10.0, 10.0))

ax1 = plt.subplot(321)
ax1.set_xlabel('Month')
ax1.set_ylabel('Revenue ($)')
ax1.set_title('Monthly Revenue - 2019')
for i, v in enumerate(monthly_revenue['Revenue']):
    ax1.text(i + .6, v + 70000, '{:,}M'.format(round(monthly_revenue['Revenue'][i+1]/1000000, 2)), fontsize=6)
ax1.bar(months, monthly_revenue['Revenue'])

ax2 = plt.subplot(322)
ax2.set_ylabel('Revenue ($)')
ax2.tick_params(axis='x', labelrotation=90, labelsize=8)
ax2.set_title('Revenue by City - 2019')
for i, v in enumerate(city_revenue['Revenue']):
    ax2.text(i - .4, v + 70000, '{:,}M'.format(round(city_revenue['Revenue'][i]/1000000, 2)), fontsize=6)
ax2.bar(cities, city_revenue['Revenue'])

ax3 = plt.subplot(312)
ax3.set_title('Orders Per Hour')
ax3.set_xlabel('Hour')
ax3.set_xticks(hours)
ax3.set_ylabel('No. of Orders')
ax3.plot(hours, hourly_orders)
plt.grid()

ax4 = plt.subplot(313)
ax4.set_title('Products by Order and Revenue')
ax4.set_xlabel('Product')
ax4.tick_params(axis='x', labelrotation=90, labelsize=8)
ax4.set_ylabel('Revenue')
ax4.bar(items_by_rev, items_revenue['Revenue'])
ax5 = ax4.twinx()
ax5.set_ylabel('Quantity Ordered', color='g')
ax5.plot(items_by_rev, items_revenue['Quantity Ordered'], color='g')
plt.grid()

plt.tight_layout()
plt.subplots_adjust(hspace=.70)
plt.show()
all_sales.to_csv('All_Sales_2019.csv')