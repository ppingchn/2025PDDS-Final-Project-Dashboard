# Library imports & Setup
import plotly.express as px
import plotly.graph_objects as go
import pandas as pd
from ..db_service import get_connection, extract_query_from_file

# Global Variables (if any)



# Visualization Functions for Tab 1: Strategy Tab

# Visualize of Global Revenue Map (Choropleth)



# Visualize of Customer Value Matrix (Scatter Plot)


# Visualization Functions for Tab 2: Operation Tab

# Visualize of Product Issues Pareto (Bar + Line)
def get_product_performance():
    # Get DB Connection
    conn = get_connection()
    
    # Extract SQL Query
    query = extract_query_from_file("get_product_performance.sql")
    if query is None:
        return None  # Exit if query could not be read

    # Execute Query and Fetch Data
    df = pd.read_sql_query(query, conn)
    
    # Close Connection
    conn.close()
    
    # Visualization Part


    return df

# Visualize of Service Quality Over Time (Line Chart)