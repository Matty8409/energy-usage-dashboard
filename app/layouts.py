import dash_bootstrap_components as dbc
from dash import html, dcc
from app.data_processing import load_initial_csv_data, apply_pulse_ratios
from app.config import pulse_ratios, energy_meter_options


def get_dashboard_layout():
    initial_df = load_initial_csv_data()
    initial_df = apply_pulse_ratios(initial_df, pulse_ratios)

    dashboard_layout = html.Div(id='theme-wrapper', children=[
        dcc.Store(id='saved-views-store', storage_type='local'),
        html.H1('Energy Usage Dashboard', className='header-title'),
        dcc.Link('Go to Register Page', href='/register'),
        html.Div([
            dcc.Input(id='save-name-input', type='text', placeholder='Enter view name...'),
            html.Button('Save View', id='save-view-button', n_clicks=0)
        ]),
        dcc.Dropdown(id='saved-view-dropdown', placeholder='Load a saved view...'),
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
                    dcc.RadioItems(
                        id='theme-toggle',
                        options=[
                            {'label': 'Light Mode', 'value': 'light'},
                            {'label': 'Dark Mode', 'value': 'dark'}
                        ],
                        value='light',
                        labelStyle={'display': 'inline-block', 'margin-right': '1rem'},
                        style={'margin-bottom': '20px'}
                    ),
                    dcc.Store(id='theme-store', storage_type='session')
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
        dcc.Store(id='data-store', data=initial_df.to_dict('records'))
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
        dcc.Link('Go to Dashboard', href='/dashboard'),
        dcc.Input(id='register-username', type='text', placeholder='Enter Username', style={'margin': '10px'}),
        dcc.Input(id='register-password', type='password', placeholder='Enter Password', style={'margin': '10px'}),
        html.Button('Register', id='register-button', n_clicks=0),
        html.Button('Go to Login', id='go-to-login', n_clicks=0, style={'marginTop': '10px'}),
        html.Div(id='register-message', style={'color': 'red', 'marginTop': '10px'}),
        # Hidden login elements
        dcc.Input(id='username', type='text', placeholder='Enter Username', style={'display': 'none'}),
        dcc.Input(id='password', type='password', placeholder='Enter Password', style={'display': 'none'}),
        html.Button('Login', id='login-button', n_clicks=0, style={'display': 'none'}),
        html.Button('Go to Register', id='go-to-register', n_clicks=0, style={'display': 'none'}),
        html.Div(id='login-message', style={'display': 'none'})
    ])
    return register_layout
