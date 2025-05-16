from dash import html, dcc
from app.layouts.navigation_bar import get_navigation_bar

def get_statistics_layout(data):
    statistics_layout = html.Div(id='theme-wrapper', children=[
        html.H1("Energy Usage Statistics", className='header-title'),
        dcc.Dropdown(
            id='statistics-energy-type-dropdown',
            options=[
                {'label': 'Electricity (kWh)', 'value': 'TH-E-01 kWh (kWh) [DELTA] 1'},
                {'label': 'Gas (kWh)', 'value': 'TH-PM-01.TH-G-01 kWh (kWh) [DELTA] 1'},
                {'label': 'Water 1 (kWh)', 'value': 'TH-PM-01.TH-W-01 kWh (kWh) [DELTA] 1'},
                {'label': 'Water 2 (kWh)', 'value': 'TH-PM-01.TH-W-02 kWh (kWh) [DELTA] 1'}
            ],
            value='TH-E-01 kWh (kWh) [DELTA] 1',
            placeholder='Select Energy Type',
            className='statistics-energy-type-dropdown'
        ),
        html.Div(id='statistics-output', className='statistics-container'),
        get_navigation_bar('/statistics')  # Add navigation bar
    ])
    return statistics_layout