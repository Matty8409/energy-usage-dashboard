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
                            {'label': 'Line Graph View', 'value': 'graph'}
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
        html.Div(id='output-container'),
        dcc.Dropdown(id='date-dropdown',
                     className='date-select-dropdown',
                     placeholder='Select a date'),
        dcc.Upload(id='add-file', children=html.Button("Upload File or ZIP Folder", className="button"), multiple=True),
        dcc.Store(id='data-store', data=initial_df.to_dict('records')),
        dcc.Link(html.Button('Go to Statistics', className='button', style={'marginTop': '10px'}),href='/statistics')
    ])
    return dashboard_layout

def get_login_layout():
    login_layout = html.Div(id='theme-wrapper', children=[
        html.H2("Login", style={'textAlign': 'center'}),
        dcc.Input(id='username', type='text', placeholder='Enter Username', style={'margin': '10px'}),
        dcc.Input(id='password', type='password', placeholder='Enter Password', style={'margin': '10px'}),
        html.Button('Login', id='login-button', n_clicks=0),
        html.Button('Go to Register', id='go-to-register', n_clicks=0, style={'marginTop': '10px'}),
        html.Div(id='login-message', style={'color': 'red', 'marginTop': '10px'})
    ])
    return login_layout

def get_register_layout():
    register_layout = html.Div(id='theme-wrapper', children=[
        html.H2("Register", style={'textAlign': 'center'}),
        dcc.Input(id='register-username', type='text', placeholder='Enter Username', style={'margin': '10px'}),
        dcc.Input(id='register-password', type='password', placeholder='Enter Password', style={'margin': '10px'}),
        html.Button('Register', id='register-button', n_clicks=0),
        html.Button('Go to Login', id='go-to-login', n_clicks=0, style={'marginTop': '10px'}),
        html.Div(id='register-message', className='register-message'),
        # Hidden login elements
        dcc.Input(id='username', type='text', placeholder='Enter Username', style={'display': 'none'}),
        dcc.Input(id='password', type='password', placeholder='Enter Password', style={'display': 'none'}),
        html.Button('Login', id='login-button', n_clicks=0, style={'display': 'none'}),
        dcc.Link(html.Button('Go to Register', className='go-to-register', style={'marginTop': '10px'}),href='/register'),
        html.Div(id='login-message')
    ])
    return register_layout

def get_statistics_layout():
    statistics_layout = html.Div(id='theme-wrapper', children=[
        dcc.Store(id='data-store'),
        html.H1("Energy Usage Statistics", className='header-title'),
        html.Div(id='statistics-output', className='statistics-container'),
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
            className = 'statistics-energy-type-dropdown'
        ),
        dcc.Link(html.Button('Go to Dashboard', className='button', style={'marginTop': '10px'}),href='/dashboard')
    ])
    return statistics_layout