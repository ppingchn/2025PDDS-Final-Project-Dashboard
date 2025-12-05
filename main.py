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

# Create a Dash application instance
app = Dash(__name__)

app.layout = html.Div([
    html.H1("E-commerce Data Dashboard"),

])

if __name__ == '__main__':
    app.run(debug=True)
