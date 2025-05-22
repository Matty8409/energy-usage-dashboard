from dash import html, dcc
from app.layouts.navigation_bar import get_navigation_bar
from app.config import energy_meter_options

def get_statistics_layout(data):
    statistics_layout = html.Div(id='theme-wrapper', children=[
        html.H1("Energy Usage Statistics", className='header-title'),
        dcc.Dropdown(
            id='statistics-energy-type-dropdown',
            options=energy_meter_options,  # Dynamically use options from config
            value=energy_meter_options[1]['value'] if energy_meter_options else None,
            placeholder='Select Energy Type',
            className='statistics-energy-type-dropdown'
        ),
        html.Div(id='statistics-output', className='statistics-container'),
        get_navigation_bar('/statistics')  # Add navigation bar
    ])
    return statistics_layout