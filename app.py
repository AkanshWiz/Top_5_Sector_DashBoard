#Importing libraries
import dash
from dash import dcc, html
import pandas as pd
from dash.dependencies import Input, Output
import plotly.express as px
import dash_bootstrap_components as dbc

# Data 
top_5_sector_data_month_1 = pd.read_csv('top_5_sector_data_month_1.csv')
top_5_sector_data_month_2 = pd.read_csv('top_5_sector_data_month_2.csv')
top_5_sector_data_month_3 = pd.read_csv('top_5_sector_data_month_3.csv')
top_5_sector_data_month_4 = pd.read_csv('top_5_sector_data_month_4.csv')
top_5_sector_data = pd.read_csv('top_5_sector_data.csv')

# Sectors Name
sector_names = top_5_sector_data['SECTOR_NAME'].unique()

# Dash Applicaton
app = dash.Dash(__name__, external_stylesheets=[dbc.themes.LUX])
server=app.server 

# Dropdown options
dropdown_options = [
    {'label': 'Line Plot', 'value': 'line'},
    {'label': 'Box Plot', 'value': 'box'},
    {'label': 'Violin Plot', 'value': 'violin'}
]

# Month dropdown options
month_dropdown_options = [
    {'label': 'Overall', 'value': 'Overall'},  # Added "Overall" option here
    {'label': 'January', 'value': 'Month_1'},
    {'label': 'February', 'value': 'Month_2'},
    {'label': 'March', 'value': 'Month_3'},
    {'label': 'April', 'value': 'Month_4'}
]

# Dash layout
app.layout = html.Div([
    html.H1('Growth Rate of Top 5 sectors'),
    dcc.Dropdown(
        id='dropdown',
        options=dropdown_options,
        value='line',  # Default option
        clearable=False
    ),
    dcc.Dropdown(
        id='month-dropdown',
        options=month_dropdown_options,
        value='Overall',  # Default month
        clearable=False
    ),
    dcc.Dropdown(
        id='sector-dropdown',
        options=[{'label': sector, 'value': sector} for sector in sector_names],
        multi=True,
        value=sector_names,  # Default sectors
        placeholder="Select sectors"
    ),
    html.Div(id='plot-container')
])

# Callback to update plot based on dropdown selections
@app.callback(
    Output('plot-container', 'children'),
    [Input('dropdown', 'value'),
     Input('month-dropdown', 'value'),
     Input('sector-dropdown', 'value')]
)
def update_plot(selected_option, selected_month, selected_sectors):
    if selected_month == 'Overall':
        if selected_option == 'line':
            # Plot for overall data (line plot)
            fig = px.line(top_5_sector_data[top_5_sector_data['SECTOR_NAME'].isin(selected_sectors)],
                          x='DATE1', y='Combined_Growth_rate', color='SECTOR_NAME')
        elif selected_option == 'box':
            # Plot for overall data (box plot)
            fig = px.box(top_5_sector_data[top_5_sector_data['SECTOR_NAME'].isin(selected_sectors)],
                         x='SECTOR_NAME', y='Combined_Growth_rate')
        elif selected_option == 'violin':
            # Plot for overall data (violin plot)
            fig = px.violin(top_5_sector_data[top_5_sector_data['SECTOR_NAME'].isin(selected_sectors)],
                            x='SECTOR_NAME', y='Combined_Growth_rate')
        else:
            fig = None
    else:
        # Plot for monthly data
        if selected_month == 'Month_1':
            selected_data = top_5_sector_data_month_1
        elif selected_month == 'Month_2':
            selected_data = top_5_sector_data_month_2
        elif selected_month == 'Month_3':
            selected_data = top_5_sector_data_month_3
        elif selected_month == 'Month_4':
            selected_data = top_5_sector_data_month_4
        else:
            return html.Div("Invalid month selection")

        if selected_option == 'line':
            fig = px.line(selected_data[selected_data['SECTOR_NAME'].isin(selected_sectors)],
                          x='DATE1', y='Growth_rate', color='SECTOR_NAME')
        elif selected_option == 'box':
            fig = px.box(selected_data[selected_data['SECTOR_NAME'].isin(selected_sectors)],
                         x='SECTOR_NAME', y='Growth_rate')
        elif selected_option == 'violin':
            fig = px.violin(selected_data[selected_data['SECTOR_NAME'].isin(selected_sectors)],
                            x='SECTOR_NAME', y='Growth_rate')
        else:
            fig = None

    if fig is not None:
        fig.update_layout(xaxis_title="DATE")
        return dcc.Graph(figure=fig)
    else:
        return html.Div("Invalid plot selection")

if __name__ == '__main__':
    app.run_server(debug=True)
