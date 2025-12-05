import os
import sqlite3
import pandas as pd

db_name = "ecommerce_project.db"
sql_path = "sql/"

# Create a function to get a database connection
def get_connection():
    conn = sqlite3.connect(db_name)
    return conn

# Function to extract the query from SQL file
def extract_query_from_file(filename):
    sql_path = os.path.join("sql", filename)
    try:
        with open(sql_path, 'r') as file:
            query = file.read()
        return query
    except FileNotFoundError:
        print(f"Error: The file {filename} was not found.")
        return None
