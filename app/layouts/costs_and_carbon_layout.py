import dash_bootstrap_components as dbc
from dash import html, dcc
from app.costs_and_carbon import get_conversion_factors_info
from app.layouts.navigation_bar import get_navigation_bar

def get_costs_and_carbon_layout(data):
    return html.Div(id='theme-wrapper', children=[
        html.H1("Costs and Carbon", className='header-title'),
        dcc.Dropdown(
            id='costs-energy-type-dropdown',
            options=[
                {'label': 'All Energy Types', 'value': 'all'},  # Added "All" option
                {'label': 'Electricity', 'value': 'Electricity'},
                {'label': 'Gas', 'value': 'Gas'},
                {'label': 'Water 1', 'value': 'Water 1'},
                {'label': 'Water 2', 'value': 'Water 2'}
            ],
            placeholder='Select Energy Type',
            className='mb-3',
            style={'width': '400px'}  # Adjusted width
        ),
        html.Div([
            dcc.Dropdown(
                id='costs-start-date-dropdown',
                placeholder='Select Start Date',
                className='mb-3',
                style={'width': '400px'}  # Adjusted width
            ),
            dcc.Dropdown(
                id='costs-end-date-dropdown',
                placeholder='Select End Date',
                className='mb-3',
                style={'width': '400px'}  # Adjusted width
            )
        ]),
        html.Button('Calculate', id='calculate-costs-button', className='btn btn-primary mb-3'),
        html.Div(id='costs-and-carbon-output', className='mt-3'),

        # Summary Section
        html.Hr(),
        html.H3("Summary of Costs and Carbon to Date", className='mt-4'),
        dbc.Row([
            dbc.Col(
                html.Div(id='costs-summary-output', className='mt-3', style={
                    'border': '1px solid #ccc',
                    'padding': '10px',
                    'borderRadius': '5px',
                    'backgroundColor': '#f9f9f9'
                }),
                width=6
            ),
            dbc.Col(
                html.Div(id='carbon-summary-output', className='mt-3', style={
                    'border': '1px solid #ccc',
                    'padding': '10px',
                    'borderRadius': '5px',
                    'backgroundColor': '#f9f9f9'
                }),
                width=6
            )
        ]),
        get_conversion_factors_info(),
        get_navigation_bar('/costs-and-carbon')  # Add navigation bar
    ])
