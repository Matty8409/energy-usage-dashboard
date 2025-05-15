import dash_bootstrap_components as dbc
from dash import html, dcc, dash_table
from app.data_processing import load_initial_csv_data, apply_pulse_ratios
from app.config import pulse_ratios, energy_meter_options

# Helper function for navigation bar
def get_navigation_bar(active_page):
    nav_items = [
        {'label': 'Dashboard', 'href': '/dashboard', 'color': 'info'},
        {'label': 'Statistics', 'href': '/statistics', 'color': 'success'},
        {'label': 'Collections', 'href': '/save-data-collection', 'color': 'primary'},
        {'label': 'Costs and Carbon', 'href': '/costs-and-carbon', 'color': 'warning'}
    ]
    return dbc.Navbar(
        dbc.Container([
            dbc.Nav(
                [
                    dbc.NavItem(
                        dcc.Link(
                            dbc.Button(
                                item['label'],
                                color=item['color'],
                                className=f"me-2 {'btn-secondary' if active_page == item['href'] else ''}"
                            ),
                            href=item['href'],
                            style={'textDecoration': 'none'}
                        )
                    ) for item in nav_items
                ],
                className='d-flex justify-content-center'
            )
        ]),
        color="light",
        dark=False,
        className="mt-4"
    )

def get_dashboard_layout():
    initial_df = load_initial_csv_data()
    initial_df = apply_pulse_ratios(initial_df, pulse_ratios)

    dashboard_layout = dbc.Container(fluid=True, children=[
        dbc.Row([
            dbc.Col(html.H1('Energy Usage Dashboard'), className='mb-4 mt-4 text-center')
        ]),

        dbc.Row([
            dbc.Col(dbc.Button(
                "Show/Hide View Selector",
                id="toolbar-toggle-button",
                color="primary",
                className="mb-3"
            ), width=12, className="text-center")
        ]),

        dbc.Collapse(
            id='toolbar-collapse',
            is_open=False,
            children=[
                dbc.Row([
                    dbc.Col([
                        dcc.RadioItems(
                            id='view-type-radio',
                            options=[
                                {'label': 'Table View', 'value': 'table'},
                                {'label': 'Line Graph View', 'value': 'graph'},
                                {'label': 'Heatmap', 'value': 'heatmap'}
                            ],
                            value='table',
                            labelStyle={'display': 'inline-block', 'marginRight': '10px'}
                        )
                    ], width=12, className="text-center")
                ])
            ]
        ),

        dbc.Row([
            dbc.Col([
                dcc.Dropdown(
                    id='energy-type-dropdown',
                    options=energy_meter_options,
                    value='all',
                    placeholder='Select energy type',
                    className='mb-3',
                    style={'width': '300px'}  # Adjust width
                ),
                dcc.Dropdown(
                    id='date-dropdown',
                    placeholder='Select a date',
                    className='mb-3',
                    style={'width': '300px'}  # Adjust width
                )
            ], width=6, className='d-flex justify-content-center')  # Center the column
        ], className='d-flex justify-content-center mb-3'),

        dbc.Row([
            dbc.Col(dcc.Loading(
                id='loading-output',
                type='default',
                children=html.Div(id='output-container')
            ), width=12)
        ]),


        dbc.Row([
            dbc.Col(dcc.Upload(
                id='add-file',
                children=dbc.Button("Upload File or ZIP Folder", color="primary"),
                multiple=True
            ), width={"size": 6, "offset": 3}, className='mb-4 text-center')
        ]),
        html.Div(id='upload-message', className='text-success mt-3'),
        dbc.Row([
            dbc.Col(
                get_navigation_bar('/dashboard'),  # Add navigation bar
                width=12,  # Ensure the navigation bar spans the full width
                className='d-flex justify-content-center'  # Center the navigation bar
            )
        ])
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
        get_navigation_bar('/statistics')  # Add navigation bar
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
                        dbc.Input(
                            id='data-input',
                            type='text',
                            placeholder='Do you want to add a note to this set of data?',
                            className='mb-3'
                        ),
                        html.P("Add a note or description for this data entry (optional).", className="text-muted"),
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
                        dbc.Input(
                            id='group-name-input',
                            type='text',
                            placeholder='Enter a group name (optional)',
                            className='mb-3'
                        ),
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
                        html.H4("Preview of Data Saved", className="card-title"),
                        dash_table.DataTable(
                            id='saved-data-table',
                            columns=[
                                {"name": "Group", "id": "group_name"},
                                {"name": "Energy Type", "id": "energy_type"},
                                {"name": "Date", "id": "date"},
                                {"name": "Input", "id": "input"},
                                {"name": "Saved At", "id": "datetime"},
                                {"name": "Summary", "id": "summary"},
                            ],
                            style_cell={
                                'fontFamily': 'monospace',
                                'whiteSpace': 'normal',
                                'textAlign': 'left',
                            },
                            style_data_conditional=[
                                {
                                    'if': {'filter_query': '{energy_type} = ""'},
                                    'backgroundColor': '#f0f0f0',
                                    'fontWeight': 'bold',
                                    'fontStyle': 'italic'
                                }
                            ],
                            style_table={'overflowX': 'auto'},
                        )

                    ])
                ], className="mb-4"),
            ], width=4),
        ]),

        dcc.Store(id='saved-data-store', data=[]),
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
            ),
        ]),
        dbc.Row([
            dbc.Col(
                get_navigation_bar('/save-data-collection'),  # Add navigation bar
                width=12,  # Ensure the navigation bar spans the full width
                className='d-flex justify-content-center'  # Center the navigation bar
            )
        ])
    ])

    return save_data_collection_layout

def get_costs_and_carbon_layout():
    initial_df = load_initial_csv_data()
    initial_df = apply_pulse_ratios(initial_df, pulse_ratios)

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
        get_navigation_bar('/costs-and-carbon')  # Add navigation bar
    ])
