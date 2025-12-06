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
    fig = go.Figure()

    # Bar Chart -- Total Sales Volume
    fig.add_trace(
        go.Bar(
            x = df['category'],
            y = df['total_sales_volume'],
            name = 'Total Sales Volume',
            marker_color='indianred',
            yaxis = 'y1'
        )
    )

    # Line Chart -- Average Customer Rating
    fig.add_trace(
        go.Scatter(
            x = df['category'],
            y = df['average_customer_rating'],
            name = 'Average Customer Rating',
            marker_color='blue',
            yaxis = 'y2'
        )
    )

    # Layout Adjustments
    fig.update_layout(
        title = '<b>Product Performance Analysis</b>',
        xaxis_title = dict(title = "Product Category"),
        # # Left Y-Axis
        yaxis = dict(
            title = "Total Sales Volume",
            titlefont = dict(color = 'indianred'),
            tickfont = dict(color = 'indianred'),
        ),
        # # Right Y-Axis
        yaxis2 = dict(
            title = "Average Customer Rating (1-5)",
            titlefont = dict(color = 'blue'),
            tickfont = dict(color = 'blue'),
            overlaying = 'y',
            side = 'right',
            range = [0, 5.5]
        ),
        legend = dict(x = 0.1, y = 1.1, orientation = 'h')
    )

    return fig

# Visualize of Service Quality Over Time (Line Chart)