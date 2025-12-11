# Library imports & Setup
import plotly.express as px
from plotly.subplots import make_subplots
import plotly.graph_objects as go
import pandas as pd
from db_service import get_connection, extract_query_from_file

# Global Variables (if any)

# Global / Helper Functions (if any)
def get_country_list():
    conn = get_connection()
    df = pd.read_sql_query("SELECT DISTINCT country FROM Customers;", conn)
    conn.close()

    options = [{'label': country, 'value': country} for country in df['country']]
    return options

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
    # Make subplots with secondary y-axis
    fig = make_subplots(specs=[[{"secondary_y": True}]])

    # Bar Chart -- Total Sales Volume
    fig.add_trace(
        go.Bar(
            x = df['category'],
            y = df['total_sales_volume'],
            name = 'Total Sales Volume',
            marker_color='indianred',
            yaxis = 'y1'
        ),
        secondary_y = False,
    )

    # Line Chart -- Average Customer Rating
    fig.add_trace(
        go.Scatter(
            x = df['category'],
            y = df['average_customer_rating'],
            name = 'Average Customer Rating',
            marker_color='blue',
            yaxis = 'y2'
        ),
        secondary_y = True,
    )

    # Layout Adjustments
    fig.update_layout(
        title_text = "Product Performance Analysis",
    )

    fig.update_xaxes(title_text="Product Category")
    fig.update_yaxes(title_text="Total Sales Volume", secondary_y=False)
    fig.update_yaxes(title_text="Average Customer Rating (1-5)", secondary_y=True, range=[0, 5.5])

    return fig

# Visualize of Service Quality Over Time (Line Chart)