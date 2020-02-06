import pandas as pd
import matplotlib.pyplot as plt
import numpy as np
import os
from itertools import combinations
from collections import Counter

# Merge 12 months of bought_together together
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

# Make all bought_together correct bought_together type
all_sales['Order ID'] = pd.to_numeric(all_sales['Order ID'])
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

print(all_sales.dtypes)