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

def get_year_list():
    conn = get_connection()
    df = pd.read_sql_query("SELECT DISTINCT strftime('%Y', order_date) as year FROM Orders ORDER BY year DESC;", conn)
    conn.close()

    options = []
    for year in df['year']:
        options.append(year)
    return options

# Visualization Functions for Tab 1: Strategy Tab

# Visualize of Global Revenue Map (Choropleth)

def get_global_revenue(selected_year=None):
    # 1. Connect & Fetch ALL Data
    conn = get_connection()
    query = extract_query_from_file("get_global_revenue.sql")
    
    if query is None:
        return go.Figure()

    df = pd.read_sql_query(query, conn)
    conn.close()

    if df.empty:
        return go.Figure().update_layout(title="No Data Found")

    # --- 2. CALCULATE YEAR-OVER-YEAR GROWTH ---
    
    # Sort data to ensure shift works correctly
    df = df.sort_values(by=['country', 'year'])

    # Shift to get previous year's revenue
    df['prev_revenue'] = df.groupby('country')['total_revenue'].shift(1)

    # Calculate Growth %
    df['yoy_growth'] = ((df['total_revenue'] - df['prev_revenue']) / df['prev_revenue']) * 100

    # --- FORMATTING GROWTH LABEL (HTML Styling) ---
    def format_growth_html(x):
        if pd.isna(x):
            return "-" # First year or N/A
        elif x > 0:
            # Green Up Arrow
            return f"<span style='color:green;'>▲</span> +{x:.1f}%"
        elif x < 0:
            # Red Down Arrow
            return f"<span style='color:red;'>▼</span> {x:.1f}%"
        else:
            # Equal (0% change)
            return "-"

    df['growth_label'] = df['yoy_growth'].apply(format_growth_html)

    # --- 3. FILTER FOR SELECTED YEAR ---
    if selected_year:
        target_year = str(selected_year)
        df_plot = df[df['year'] == target_year].copy()
    else:
        # Default to latest year
        latest_year = df['year'].max()
        df_plot = df[df['year'] == latest_year].copy()
        selected_year = latest_year

    if df_plot.empty:
        return go.Figure().update_layout(title=f"No Data for {selected_year}")

    # --- 4. CREATE VISUALIZATION ---
    fig = px.scatter_geo(
        df_plot,
        locations="country",
        locationmode="country names",
        color="total_revenue",
        size="total_revenue",
        hover_name="country",
        projection="natural earth",
        title=f"Revenue Map ({selected_year})",
        template="plotly_white",
        color_continuous_scale=px.colors.sequential.Blues,
        
        # Add 'growth_label' to custom_data (Index 3)
        custom_data=['total_revenue', 'avg_basket_size', 'avg_delivery_time', 'growth_label']
    )

    # Update Tooltip with HTML support
    fig.update_traces(
        hovertemplate="<b>%{hovertext}</b><br>" +
                      "<i>Growth: %{customdata[3]}</i><br><br>" + # Shows colored arrow
                      "Total Revenue: $%{customdata[0]:,.0f}<br>" +
                      "Avg. Basket Size: $%{customdata[1]:,.0f}<br>" +
                      "Avg. Delivery Time: %{customdata[2]:.1f} days<extra></extra>"
    )
    
    # Ensure Hover Background is White
    fig.update_layout(
        hoverlabel=dict(
            bgcolor="white",
            font_size=14,
            font_family="Arial"
        ),
        coloraxis_colorbar=dict(title="Revenue ($)")
    )

    return fig

# Visualize of Customer Value Matrix (Scatter Plot)


# Visualization Functions for Tab 2: Operation Tab

#
def get_customer_matrix_plot(selected_year=None, selected_country="All Countries", return_kpis=False):
    # 1. Connect
    conn = get_connection()
    query = extract_query_from_file("get_customer_matrix.sql")
    
    if query is None:
        return go.Figure().update_layout(title="SQL Query not found.")

    # 2. Prepare Parameters for SQL
    # If selected_year is None, we pass None to SQL (activating the "IS NULL" logic)
    # We convert to string just in case, to match the SQL strftime format
    sql_year = str(selected_year) if selected_year else None
    
    # Handle "All Countries" logic
    sql_country = selected_country if selected_country != "All Countries" else None

    # We pass the parameters twice each because the SQL uses them twice:
    # (? IS NULL OR Year = ?) AND (? IS NULL OR Country = ?)
    params = (sql_year, sql_year, sql_country, sql_country)

    # 3. Execute Query with Parameters
    df = pd.read_sql_query(query, conn, params=params)
    conn.close()

    # Safety: Handle empty results
    if df.empty:
        return go.Figure().update_layout(title=f"No data for {selected_country} in {selected_year or 'All Years'}")

    # 4. Post-Processing
    # Since SQL now gives us a proper 'YYYY-MM-01' string, we just convert it directly.
    # No more manual string concatenation needed!
    df['full_date'] = pd.to_datetime(df['full_date'])

    # 5. Visualization
    fig = px.line(
        df,
        x='full_date',
        y='total_spent',
        color='country',
        markers=True,
        title=f"Customer Monthly Total Spend ({selected_year if selected_year else 'All Time'})",
        template="plotly_white",
        custom_data=['country', 'full_date', 'total_spent']
    )

    # Tooltip Styling
    fig.update_traces(
        hovertemplate="<b>Country:</b> %{customdata[0]}<br>"
                      "<b>Date:</b> %{x|%B %Y}<br>"
                      "<b>Total Spent:</b> $%{y:,.2f}<extra></extra>"
    )

    # Layout
    fig.update_layout(
        xaxis_title='Month',
        yaxis_title='Total Spent ($)',
        xaxis=dict(type='date', dtick="M1", tickformat="%b %Y"),
        hoverlabel=dict(bgcolor='white'),
        margin=dict(l=40, r=40, t=40, b=40)
    )

    return fig

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
    
    # Graph Notation Logic Section
    # --------------------------
    avg_sales_volume = df['total_sales_volume'].mean()
    avg_rating = df['average_customer_rating'].mean()

    color_conditions = []
    annotations = []

    for index, row in df.iterrows():
        if row['total_sales_volume'] < avg_sales_volume and row['average_customer_rating'] < avg_rating:
            color_conditions.append('#FF8C00')  # Red Color Added
            annotations.append('Action Needed')
        else:
            color_conditions.append('#1976D2')  # Blue Color Added
            annotations.append('')
    
    # Visualization Part
    fig = make_subplots(specs=[[{"secondary_y": True}]])

    # Bar Chart -- Total Sales Volume
    fig.add_trace(
        go.Bar(
            x = df['category'],
            y = df['total_sales_volume'],
            name = 'Total Sales Volume',
            marker_color=color_conditions,
            text=annotations,
            textposition='inside',
            insidetextanchor='start',
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

    fig.add_hline(
        y = avg_sales_volume,
        line_dash="dot",
        annotation_text="Avg Sales Volume",
        line_color="green"
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
def get_service_quality(selected_country = "All Countries"):
    # Get DB Connection
    conn = get_connection()
    
    # Extract SQL Query
    query = extract_query_from_file("get_service_quality.sql")
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

    current_country = selected_country if selected_country else "All Countries"

    # Layout Adjustments
    fig.update_layout(
        title_text = f"Service Quality Trend: Shipping Time vs Customer Satisfaction - {current_country}",
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