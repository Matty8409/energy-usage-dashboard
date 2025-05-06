import dash_bootstrap_components as dbc
from dash import html, dcc, dash_table
from app.data_processing import load_initial_csv_data, apply_pulse_ratios
from app.config import pulse_ratios, energy_meter_options


def get_dashboard_layout():
    initial_df = load_initial_csv_data()
    initial_df = apply_pulse_ratios(initial_df, pulse_ratios)

    dashboard_layout = html.Div(id='theme-wrapper', children=[
        html.H1('Energy Usage Dashboard', className='header-title'),
        dbc.Button(
            "Show/Hide View Selector",  # Button text
            id="toolbar-toggle-button",  # Button ID
            color="primary",  # Button color
            className="mb-3",  # Add margin below the button
            n_clicks=0  # Initialize click count
        ),
        dbc.Collapse(
            id='toolbar-collapse',
            is_open=True,  # Initially collapsed
            children=[
                html.Div(id='toolbar', className='toolbar', children=[
                    dcc.RadioItems(
                        id='view-type-radio',
                        options=[
                            {'label': 'Table View ', 'value': 'table'},
                            {'label': 'Line Graph View ', 'value': 'graph'},
                            {'label': 'Heat map ', 'value': 'heatmap'}
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
        dcc.Input(id='register-username', style={'display': 'none'}),
        dcc.Input(id='register-password', style={'display': 'none'}),
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
        dcc.Input(id='register-username', value='', type='text', style={'display': 'none'}),
        dcc.Input(id='register-password', value='', type='password', style={'display': 'none'}),
        html.Button('Login', id='login-button', n_clicks=0, className='me-1 mt-1 btn btn-primary' ,style={'display': 'none'}),
        html.Div(id='login-message')
    ])
    return register_layout

def get_statistics_layout():
    initial_df = load_initial_csv_data()
    initial_df = apply_pulse_ratios(initial_df, pulse_ratios)

    statistics_layout = html.Div(id='theme-wrapper', children=[
        dcc.Store(id='data-store', data=initial_df.to_dict('records')),
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
        dcc.Link(html.Button('Go to Dashboard', className='me-1 mt-1 btn btn-primary', style={'marginTop': '10px'}),href='/dashboard')
    ])
    return statistics_layout


def get_save_data_collection_layout():
    initial_df = load_initial_csv_data()
    initial_df = apply_pulse_ratios(initial_df, pulse_ratios)

    save_data_collection_layout = dbc.Container(fluid=True, children=[
        html.H2("Save and Collect Data", className="text-center my-4"),

        dbc.Row([
            dbc.Col([
                dbc.Card([
                    dbc.CardBody([
                        html.H4("Enter Data", className="card-title"),
                        dbc.Input(id='data-input', type='text', placeholder='Enter data', className='mb-3'),
                        html.P("Enter a custom label or identifier for this data entry (optional).",
                               className="text-muted"),
                        html.P("Select the type of energy and date you want to save.", className="text-muted"),
                        dbc.Row([
                            dbc.Col([
                                dcc.Dropdown(
                                    id='energy-type-dropdown',
                                    options=energy_meter_options,
                                    value='all',
                                    placeholder="Select Energy Type",
                                    className='mb-3'
                                )
                            ], width=6),
                            dbc.Col([
                                dcc.Dropdown(
                                    id='date-dropdown',
                                    placeholder='Select a date',
                                    className='mb-3'
                                )
                            ], width=6),
                        ]),
                        dbc.Input(id='group-name-input', type='text', placeholder='Enter group name', className='mb-3'),
                        dbc.Button('Save Data', id='save-data-button', color='primary', className='w-100'),
                        html.Div(id='save-data-message', className='text-success mt-3'),
                    ])
                ], className="mb-4"),
            ], width=4),

            dbc.Col([
                dbc.Card([
                    dbc.CardBody([
                        html.H4("Download Options", className="card-title"),
                        dcc.Dropdown(
                            id="group-selection-dropdown",
                            placeholder="Select a group or ungrouped data",
                            className="mb-3"
                        ),
                        dbc.Button("Download Selected Group", id="download-button", color="success",
                                   className="w-100 mb-3"),
                        dcc.Download(id="download-component"),
                        html.H5("Group Summary", className="mt-4"),
                        html.Div(id="group-summary", className="mt-3 text-muted"),
                        html.H5("Saved Summary Stats", className="mt-4"),
                        html.Div(id="saved-summary-stats", className="mt-3 text-muted"),
                    ])
                ], className="mb-4"),
            ], width=4),

            dbc.Col([
                dbc.Card([
                    dbc.CardBody([
                        html.H4("Preview of Data saved", className="card-title"),
                        dash_table.DataTable(
                            id='saved-data-table',
                            columns=[
                                {'name': 'Energy Type', 'id': 'energy_type'},
                                {'name': 'Date', 'id': 'date'},
                                {'name': 'Label', 'id': 'input'},
                                {'name': 'Saved At', 'id': 'datetime'},
                                {'name': 'Summary', 'id': 'summary'}
                            ],
                            data=[],  # Will be populated by the callback
                            page_size=10,
                            style_table={'overflowX': 'auto'},
                            style_cell={'textAlign': 'left', 'padding': '10px'},
                            style_header={'backgroundColor': 'lightgrey', 'fontWeight': 'bold'}
                        )
                    ])
                ], className="mb-4"),
            ], width=4),
        ]),

        dcc.Store(id='saved-data-store', data=[]),
        dcc.Store(id='data-store', data=initial_df.to_dict('records')),
        html.H4("Preview Section", className="text-muted mt-4"),
        html.P(
            "This section allows you to preview the data based on your current selections for date and energy type. "
            "Click the button below to show or hide the preview.",
            className="text-muted"
        ),
        html.Div([
            dbc.Button(
                "Show Preview",  # Default button text
                id="toggle-preview-button",
                color="primary",
                className="mb-3",
                n_clicks=0
            ),
            dbc.Tooltip(
                "Click to toggle the preview of your selected data.",
                target="toggle-preview-button"
            ),
            dbc.Collapse(
                id="preview-collapse",
                is_open=False,  # Initially hidden
                children=[
                    dcc.RadioItems(
                        id='view-type-radio',
                        options=[
                            {'label': 'Table View', 'value': 'table'},
                            {'label': 'Line Graph View', 'value': 'graph'}
                        ],
                        value='table',
                        labelStyle={'display': 'inline-block'},
                        className="mb-3"
                    ),
                    html.Div(
                        id='output-container',
                        style={
                            'border': '1px solid #ccc',
                            'padding': '10px',
                            'borderRadius': '5px',
                            'backgroundColor': '#f9f9f9'
                        }
                    )
                ]
            )
        ])
    ])

    return save_data_collection_layout