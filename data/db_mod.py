import pandas as pd
import sqlite3
import numpy as np
from datetime import timedelta

# 1. Load the Raw Data
df = pd.read_csv('ecommerce_dataset_10000.csv')

# --- DATA PREPARATION & CLEANING ---

# Convert dates to datetime objects
df['order_date'] = pd.to_datetime(df['order_date'])
df['signup_date'] = pd.to_datetime(df['signup_date'])
df['review_date'] = pd.to_datetime(df['review_date'])

# FIX: Synthesize 'delivery_date' since it's missing (Required for Vis 1 & 4)
# Logic: Delivery takes between 2 to 7 days after order
np.random.seed(42) # For reproducibility
random_days = np.random.randint(2, 8, size=len(df))
df['delivery_date'] = df['order_date'] + pd.to_timedelta(random_days, unit='D')

# Ensure unit_price is a float for math
df['unit_price'] = df['unit_price'].astype(float)


# --- 3NF NORMALIZATION (Splitting into 5 Tables) ---

# 1. CUSTOMERS Table
customers = df[['customer_id', 'first_name', 'country', 'age_group', 'signup_date']].drop_duplicates(subset=['customer_id'])

# 2. ORDERS Table
orders = df[['order_id', 'customer_id', 'order_date', 'delivery_date', 'order_status']].drop_duplicates(subset=['order_id'])

# 3. PRODUCTS Table
products = df[['product_id', 'product_name', 'category']].drop_duplicates(subset=['product_id'])

# 4. ORDER_ITEMS Table
# In this specific dataset, 1 row = 1 item. We map it directly.
order_items = df[['order_id', 'product_id', 'quantity', 'unit_price']].copy()
# Create a unique ID for each item row (optional but good practice)
order_items['order_item_id'] = range(1, len(order_items) + 1)

# 5. REVIEWS Table
reviews = df[['review_id', 'order_id', 'rating', 'review_date']].drop_duplicates(subset=['review_id'])


# --- SAVE TO SQLITE ---

db_name = "ecommerce.db"
conn = sqlite3.connect(db_name)

# Write tables to database
customers.to_sql('Customers', conn, if_exists='replace', index=False)
orders.to_sql('Orders', conn, if_exists='replace', index=False)
products.to_sql('Products', conn, if_exists='replace', index=False)
order_items.to_sql('Order_Items', conn, if_exists='replace', index=False)
reviews.to_sql('Reviews', conn, if_exists='replace', index=False)

conn.close()

print(f"Successfully created {db_name} with 5 tables!")
print("Tables created: Customers, Orders, Products, Order_Items, Reviews")