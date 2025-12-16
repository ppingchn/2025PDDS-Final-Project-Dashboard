# Import Dash core libraries
from dash import Dash, dcc, html, Input, Output, callback

# Import data manipulation and visualization libraries
import pandas as pd
import plotly.express as px
import plotly.graph_objects as go

# Import additional utilities
import sqlite3
import numpy as np
from datetime import datetime

# Import Visualization functions from visual.py
from visual import get_product_performance, get_country_list, get_service_quality, get_global_revenue, get_year_list, get_customer_matrix_plot

# Data fetching
country_options = get_country_list()
year_options = get_year_list()

# --- CSS STYLES CONFIGURATION ---
THEME = {
    'background': '#F0F2F5',      
    'card_bg': '#FFFFFF',         
    'primary': '#0052CC',         
    'text': '#172B4D',            
    'text_light': '#6B778C',      
    'border': '#DFE1E6',          
    'shadow': '0 4px 6px rgba(0, 0, 0, 0.1)' 
}


graph_wrapper_style = {
    'width': '90%',       
    'margin': '0 auto',   
    'display': 'block'
}

tabs_styles = {
    'height': '44px',
    'alignItems': 'center',
    'borderBottom': f'1px solid {THEME["border"]}'
}
tab_style = {
    'borderBottom': '1px solid #d6d6d6',
    'padding': '12px',
    'fontWeight': 'bold',
    'color': THEME['text_light'],
    'backgroundColor': '#FAFBFC'
}
tab_selected_style = {
    'borderTop': f'3px solid {THEME["primary"]}',
    'borderBottom': '1px solid #d6d6d6',
    'backgroundColor': 'white',
    'color': THEME['primary'],
    'padding': '12px',
    'fontWeight': 'bold'
}

card_container_style = {
    'backgroundColor': THEME['card_bg'],
    'borderRadius': '8px',
    'boxShadow': THEME['shadow'],
    'padding': '24px',
    'marginBottom': '24px',
    'border': f'1px solid {THEME["border"]}'
}

header_style = {
    'backgroundColor': 'white',
    'padding': '25px 30px',
    'borderRadius': '12px',
    'marginBottom': '30px',
    'boxShadow': '0 4px 20px rgba(0, 82, 204, 0.1)', # เงาสีฟ้านุ่มๆ
    'display': 'flex',
    'flexDirection': 'column',
    'borderLeft': f'6px solid {THEME["primary"]}' # เส้น Accent สีน้ำเงินด้านซ้าย
}

# Create a Dash application instance
app = Dash(__name__)

app.layout = html.Div(style={'backgroundColor': THEME['background'], 'fontFamily': 'Segoe UI, Roboto, Helvetica, Arial, sans-serif', 'minHeight': '100vh', 'padding': '20px'}, children=[
    
    # --- HEADER ---
    html.Div(style=header_style, children=[
        html.Div([
            html.Span("📊", style={'fontSize': '32px', 'marginRight': '15px'}),
            html.Div([
                html.H1("3PY E-COMMERCE", style={
                    'color': THEME['primary'], 
                    'fontSize': '28px', 
                    'marginBottom': '0', 
                    'fontWeight': '800',
                    'letterSpacing': '1px'
                }),
                html.P("Global Growth Dashboard: Strategic & Operational Overview", style={
                    'color': THEME['text_light'], 
                    'fontSize': '16px', 
                    'marginTop': '5px',
                    'fontWeight': '500'
                })
            ])
        ], style={'display': 'flex', 'alignItems': 'center'})
    ]),

    # --- TABS ---
    dcc.Tabs(style=tabs_styles, children=[
        
        # === TAB 1: STRATEGY ===
        dcc.Tab(label='Strategy Overview', style=tab_style, selected_style=tab_selected_style, children=[
            html.Div(style={'padding': '20px'}, children=[
                
                # Card: Revenue Map
                html.Div(style=card_container_style, children=[
                    html.Div([
                        html.Div([
                            html.H2("Global Revenue Visualization", style={'fontSize': '22px', 'color': THEME['text'], 'marginBottom': '10px'}),
                            html.P("Overview of total revenue and efficiency across different regions.", style={'color': THEME['text_light'], 'fontSize': '14px'})
                        ], style={'width': '60%'}),
                        
                        html.Div([
                            html.Label("Select Year:", style={'fontWeight': 'bold', 'marginRight': '10px', 'color': THEME['text']}),
                            dcc.Dropdown(
                                id='year-filter',
                                options=year_options,
                                value=year_options[0] if year_options else None,
                                clearable=False,
                                style={'width': '150px'}
                            )
                        ], style={'width': '40%', 'display': 'flex', 'justifyContent': 'flex-end', 'alignItems': 'center'})
                    ], style={'display': 'flex', 'justifyContent': 'space-between', 'alignItems': 'start', 'marginBottom': '20px'}),
                    
                    # Graph: Map wrapped in centering div
                    html.Div(style=graph_wrapper_style, children=[
                        dcc.Graph(
                            id='global-revenue-graph',
                            style={'height': '80vh'} 
                        )
                    ])
                ]),
                # Card: Customer Value Matrix
                html.Div(style=card_container_style, children=[
                    html.Div([
                        html.Div([
                            html.H2("Customer Value Matrix", style={'fontSize': '22px', 'color': THEME['text'], 'marginBottom': '10px'})
                        ], style={'width': '60%'}),
                        html.Div([
                            html.Label("Select Country:", style={'fontWeight': 'bold', 'marginRight': '10px', 'color': THEME['text']}),
                            dcc.Dropdown(
                                id='customer-country-filter',
                                options=country_options,
                                value='All Countries',
                                clearable=False,
                                style={'width': '250px'}
                            )
                        ], style={'width': '40%', 'display': 'flex', 'justifyContent': 'flex-end', 'alignItems': 'center'})
                    ], style={'display': 'flex', 'justifyContent': 'space-between', 'alignItems': 'start', 'marginBottom': '20px'}),
                    # Graph: Customer Matrix wrapped in centering div
                    html.Div(style=graph_wrapper_style, children=[
                        dcc.Graph(
                            id='customer-matrix-graph',
                            style = {'height': '80vh'}
                        ),
                    ]),
                ]),
            ])
        ]),

        # === TAB 2: OPERATIONS ===
        dcc.Tab(label='Operational Information', style=tab_style, selected_style=tab_selected_style, children=[
            html.Div(style={'padding': '20px'}, children=[
                
                # Filter Section
                html.Div(style=card_container_style, children=[
                    html.Label("Filter by Country:", style={'fontWeight': 'bold', 'marginBottom': '10px', 'display': 'block', 'color': THEME['text']}),
                    dcc.Dropdown(
                        id='country-filter',
                        options=country_options,
                        value=None,
                        placeholder="Select a Country to analyze specific performance...",
                        clearable=True,
                        style={'width': '100%', 'maxWidth': '400px'}
                    )
                ]),

                # Card: Product Performance
                html.Div(style=card_container_style, children=[
                    html.H2("Product Performance Analysis", style={'fontSize': '22px', 'color': THEME['text'], 'marginBottom': '20px'}),
                    # Graph wrapper
                    html.Div(style=graph_wrapper_style, children=[
                        dcc.Graph(
                            id='product-performance-graph',
                            style={'height': '500px'} 
                        )
                    ])
                ]),

                # Card: Service Quality
                html.Div(style=card_container_style, children=[
                    html.H2("Service Quality Over Time", style={'fontSize': '22px', 'color': THEME['text'], 'marginBottom': '20px'}),
                    # Graph wrapper
                    html.Div(style=graph_wrapper_style, children=[
                        dcc.Graph(
                            id='service-quality-graph',
                            style={'height': '500px'}
                        )
                    ])
                ])
            ])
        ])
    ])
])

# --- CALLBACKS ---

@callback(
    [
        Output('product-performance-graph', 'figure'),
        Output('service-quality-graph', 'figure'),
    ],
    Input('country-filter', 'value')
)
def update_product_performance(selected_country):
    fig_product, fig_service = get_product_performance(selected_country), get_service_quality(selected_country)
    
    # Style Product Graph
    # fig_product.update_traces(marker_color=THEME['primary'], selector=dict(type='bar'))
    fig_product.update_traces(line_color='#FFAB00', selector=dict(type='scatter')) 
    
    fig_product.update_layout(
        paper_bgcolor='white',
        plot_bgcolor='white',
        font={'family': 'Segoe UI, sans-serif', 'color': THEME['text']},
        margin=dict(l=40, r=40, t=40, b=40)
    )

    # Style Service Graph
    fig_service.update_traces(line_color='#FFAB00', selector=dict(name='Avg Shipping Days')) 
    fig_service.update_traces(line_color=THEME['primary'], selector=dict(name='Avg Review Score'))
    
    fig_service.update_layout(
        paper_bgcolor='white',
        plot_bgcolor='white',
        font={'family': 'Segoe UI, sans-serif', 'color': THEME['text']},
        margin=dict(l=40, r=40, t=40, b=40),
        legend=dict(orientation="h", yanchor="bottom", y=1.02, xanchor="right", x=1)
    )

    return fig_product, fig_service

@callback(
    Output('global-revenue-graph', 'figure'),
    Input('year-filter', 'value')
)
def update_global_revenue(selected_year):
    fig_map = get_global_revenue(selected_year)
    
    
    fig_map.update_layout(
        paper_bgcolor='white',
        plot_bgcolor='white',
        font={'family': 'Segoe UI, sans-serif', 'color': THEME['text']},
        margin=dict(l=0, r=0, t=30, b=0),
        geo=dict(
            bgcolor='white',            
            showland=True,              
            landcolor="#EAE7E7",       
            countrycolor='white',       
            showcoastlines=False,       
            showframe=False,            
            projection_type='natural earth'
        )
    )
    
    return fig_map

@callback(
    Output('customer-matrix-graph', 'figure'),[
    Input('year-filter', 'value'),
    Input('customer-country-filter', 'value')
    ]
)
def update_customer_matrix(selected_year,selected_country):
    return get_customer_matrix_plot(selected_year=selected_year,selected_country=selected_country)

if __name__ == '__main__':
    app.run(debug=True)