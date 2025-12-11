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

    options = ['All Countries']
    for country in df['country']:
        options.append(country)
    return options

# Visualization Functions for Tab 1: Strategy Tab

# Visualize of Global Revenue Map (Choropleth)



# Visualize of Customer Value Matrix (Scatter Plot)


# Visualization Functions for Tab 2: Operation Tab

# Visualize of Product Issues Pareto (Bar + Line)
def get_product_performance(selected_country = "All Countries"):
    # Get DB Connection
    conn = get_connection()
    
    # Extract SQL Query
    query = extract_query_from_file("get_product_performance.sql")
    if query is None:
        return None  # Exit if query could not be read
    # Parameterize Query
    if selected_country == "All Countries":
        # Execute Query and Fetch Data
        params = (None, None)
    else:
        params = (selected_country, selected_country)

    df = pd.read_sql_query(query, conn, params=params)
    
    # Close Connection
    conn.close()

    if df.empty:
        print("No data available for the selected country.")
        return go.Figure().update_layout(title="No data available for the selected country.")
    
    # Visualization Part
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
    fig.update_yaxes(title_text="Total Sales Volume", secondary_y=False, autorange=True)
    fig.update_yaxes(title_text="Average Customer Rating (1-5)", secondary_y=True, autorange=True)

    # Update title
    current_country = selected_country if selected_country else "All Countries"
    fig.update_layout(title_text=f"Product Performance Analysis - {current_country}")

    return fig

# Visualize of Service Quality Over Time (Line Chart)
# Visualize Service Quality Trend (Line + Line)
def get_service_quality():
    # Get DB Connection
    conn = get_connection()
    
    # Extract SQL Query
    query = extract_query_from_file("get_service_quality.sql")
    if query is None:
        return None  # Exit if query could not be read

    # Execute Query and Fetch Data
    df = pd.read_sql_query(query, conn)
    
    # Close Connection
    conn.close()
    
    # Convert month column to datetime for plotting
    df['month'] = pd.to_datetime(df['month'])

    # --------------------------
    # Visualization Part
    # --------------------------
    fig = make_subplots(specs=[[{"secondary_y": True}]])

    # Line 1 -- Avg Shipping Days
    fig.add_trace(
        go.Scatter(
            x = df['month'],
            y = df['avg_shipping_days'],
            name = 'Avg Shipping Days',
            marker_color='orange',
            mode='lines+markers',
            yaxis='y1'
        ),
        secondary_y = False,
    )

    # Line 2 -- Avg Review Score
    fig.add_trace(
        go.Scatter(
            x = df['month'],
            y = df['avg_review_score'],
            name = 'Avg Review Score',
            marker_color='blue',
            mode='lines+markers',
            yaxis='y2'
        ),
        secondary_y = True,
    )

    # Layout Adjustments
    fig.update_layout(
        title_text = "Service Quality Trend: Shipping Time vs Customer Satisfaction",
        hovermode='x unified'
    )

    # X-axis
    fig.update_xaxes(
        title_text="Time (Monthly)",
        rangeslider=dict(visible=True),
        type='date'
    )

    # Left Y-axis
    fig.update_yaxes(
        title_text="Avg Shipping Days",
        secondary_y=False
    )

    # Right Y-axis
    fig.update_yaxes(
        title_text="Avg Review Score (1-5)",
        secondary_y=True,
        range=[0, 5.5]
    )

    return fig