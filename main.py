# Import Dash core libraries
from dash import Dash, dcc, html, Input, Output, callback

# Import data manipulation and visualization libraries
import pandas as pd
import plotly.express as px
import plotly.graph_objects as go

# Import additional utilities (optional, add as needed)
import sqlite3
import numpy as np
from datetime import datetime

# Import Visualization functions from visual.py
from visual import get_product_performance, get_country_list, get_service_quality

# Data fetching
country_options = get_country_list()

# Create a Dash application instance
app = Dash(__name__)

app.layout = html.Div([
    html.H1("Global Growth Dashboard"),

    dcc.Tabs([
        dcc.Tab(label='Strategy', children=[
            # Pleaceholders for Tab 1
        ]),
        dcc.Tab(label='Operations', children=[
            html.H2("Product Performance Analysis"),
            html.Div([
                dcc.Dropdown(
                    id = 'country-filter',
                    options = country_options,
                    value = None,
                    placeholder = "Select a Country",
                    clearable = True,
                    style = {'width': '50%'}
                )
            ], style={'padding': '20px'}
            ),
            dcc.Graph(
                id='product-performance-graph'
            ),
            # Placeholders for Tab 2
            html.H2("Service Quality Over Time"),
            dcc.Graph(
                id = 'service-quality-graph'
            )
        ])
    ])
])

# Callback for interactivity
@callback(
    [
        Output('product-performance-graph', 'figure'),
        Output('service-quality-graph', 'figure')
    ],
    Input('country-filter', 'value')
)
def update_product_performance(selected_country):
    return get_product_performance(selected_country), get_service_quality(selected_country)

if __name__ == '__main__':
    app.run(debug=True)
