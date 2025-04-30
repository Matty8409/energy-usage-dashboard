import dash_bootstrap_components as dbc
from dash import html, dcc
from app.data_processing import load_initial_csv_data, apply_pulse_ratios
from app.config import pulse_ratios, energy_meter_options


def get_dashboard_layout():
    initial_df = load_initial_csv_data()
    initial_df = apply_pulse_ratios(initial_df, pulse_ratios)

    dashboard_layout = html.Div(id='theme-wrapper', children=[
        html.H1('Energy Usage Dashboard', className='header-title'),
        dbc.Collapse(
            id='toolbar-collapse',
            is_open=False,  # Initially collapsed
            children=[
                html.Div(id='toolbar', className='toolbar', children=[
                    dcc.RadioItems(
                        id='view-type-radio',
                        options=[
                            {'label': 'Table View', 'value': 'table'},
                            {'label': 'Line Graph View', 'value': 'graph'},
                            {'label': 'Heat map', 'value': 'heatmap'}
                        ],
                        value='table',
                        labelStyle={'display': 'inline-block'}
                    ),
                ])
        ]
        ),
        dcc.Dropdown(
            id='energy-type-dropdown',
            options=energy_meter_options,
            value='all',
            className='energy-type-dropdown'
        ),
        html.Div(
            id='output-wrapper',
            children=[
                dcc.Loading(
                    id='loading-output',
                    type='default',  # spinner type (optional)
                    children=html.Div(id='output-container')
                )
            ]
        ),
        dcc.Dropdown(id='date-dropdown',
                     className='date-select-dropdown',
                     placeholder='Select a date'),
        dcc.Upload(id='add-file', children=html.Button("Upload File or ZIP Folder", className="me-1 mt-1 btn btn-primary"), multiple=True),
        dcc.Store(id='data-store', data=initial_df.to_dict('records')),
        dcc.Link(html.Button('Go to Statistics', className='me-1 mt-1 btn btn-primary', style={'marginTop': '10px'}),href='/statistics')
    ])
    return dashboard_layout

def get_login_layout():
    login_layout = dbc.Container([
        html.H2("Login", className="text-center my-4"),
        dbc.Input(id='username', type='text', placeholder='Enter Username', className='mb-3 login-input'),
        dbc.Input(id='password', type='password', placeholder='Enter Password', className='mb-3 login-input'),
        html.Div([
            dbc.Button('Login', id='login-button', color='primary', className='btn-primary login-button'),
            dbc.Button('Go to Register', id='go-to-register', color='primary', className='btn-primary login-button')
        ], className='login-button-group'),
        html.Div(id='login-message', className='text-danger mt-3')
    ], id='theme-wrapper', className='p-4')
    return login_layout

def get_register_layout():
    register_layout = html.Div(id='theme-wrapper', children=[
        html.H2("Register", style={'textAlign': 'center'}),
        dcc.Input(id='register-username', type='text', placeholder='Enter Username', style={'margin': '10px'}),
        dcc.Input(id='register-password', type='password', placeholder='Enter Password', style={'margin': '10px'}),
        html.Button('Register', id='register-button', n_clicks=0),
        html.Button('Go to Login', id='go-to-login', n_clicks=0, className='me-1 mt-1 btn btn-primary', style={'marginTop': '10px'}),
        html.Div(id='register-message', className='register-message'),
        # Hidden login elements
        dcc.Input(id='username', type='text', placeholder='Enter Username', style={'display': 'none'}),
        dcc.Input(id='password', type='password', placeholder='Enter Password', style={'display': 'none'}),
        html.Button('Login', id='login-button', n_clicks=0, className='me-1 mt-1 btn btn-primary' ,style={'display': 'none'}),
        html.Div(id='login-message')
    ])
    return register_layout

def get_statistics_layout():
    statistics_layout = html.Div(id='theme-wrapper', children=[
        dcc.Store(id='data-store'),
        html.H1("Energy Usage Statistics", className='header-title'),
        dcc.Dropdown(
            id='statistics-energy-type-dropdown',
            options=[
                {'label': 'All Energy Types', 'value': 'all'},
                {'label': 'Electricity (kWh)', 'value': 'TH-E-01 kWh (kWh) [DELTA] 1'},
                {'label': 'Gas (kWh)', 'value': 'TH-PM-01.TH-G-01 kWh (kWh) [DELTA] 1'},
                {'label': 'Water 1 (kWh)', 'value': 'TH-PM-01.TH-W-01 kWh (kWh) [DELTA] 1'},
                {'label': 'Water 2 (kWh)', 'value': 'TH-PM-01.TH-W-02 kWh (kWh) [DELTA] 1'}
            ],
            value='all',
            placeholder='Select Energy Type',
            className='statistics-energy-type-dropdown'
        ),
        html.Div(id='statistics-output', className='statistics-container'),
        dcc.Link(html.Button('Go to Dashboard', className='button', style={'marginTop': '10px'}),href='/dashboard')
    ])
    return statistics_layout

def get_save_data_collection_layout():
    save_data_collection_layout = html.Div(id='theme-wrapper', children=[
        html.H2("Save and Collect Data", style={'textAlign': 'center'}),
        dcc.Input(id='data-input', type='text', placeholder='Enter data', style={'margin': '10px'}),

        dcc.Dropdown(
            id='energy-type-dropdown',
            options=energy_meter_options,
            value='all',  # Default value
            style={'margin': '10px'}
        ),
        dcc.Dropdown(id='date-dropdown',
                     className='date-select-dropdown',
                     placeholder='Select a date'),

        html.Button('Save Data', id='save-data-button', n_clicks=0, style={'margin': '10px'}),
        html.Div(id='save-data-message', style={'color': 'green', 'marginTop': '10px'}),
        html.Hr(),
        html.H3("Saved Data", style={'textAlign': 'center'}),
        html.Div(id='saved-data-display'),
        dcc.Store(id='saved-data-store', data=[]),  # Store to hold saved data
        dcc.Store(id='data-store', data=[]),
        dcc.RadioItems(
            id='view-type-radio',
            options=[
                {'label': 'Table View', 'value': 'table'},
                {'label': 'Line Graph View', 'value': 'graph'}
            ],
            value='table',
            labelStyle={'display': 'inline-block'}
        ),
        html.Div(id='output-container'),  # Ensure this is included
    ])
    return save_data_collection_layout

