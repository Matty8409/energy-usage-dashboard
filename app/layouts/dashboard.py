import dash_bootstrap_components as dbc
from dash import html, dcc
from app.config import energy_meter_options
from app.layouts.navigation_bar import get_navigation_bar

def get_dashboard_layout(data):
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
            dbc.Col(
                dcc.Dropdown(
                    id='energy-type-dropdown',
                    options=energy_meter_options,
                    value='all',
                    placeholder='Select energy type',
                    className='mb-3',
                    style={'width': '300px'}  # Adjust width
                ),
                width=6, className='d-flex justify-content-center'  # Center the column
            )
        ], className='d-flex justify-content-center mb-3'),

        dbc.Row([
            dbc.Col(
                dcc.Dropdown(
                    id='date-dropdown',
                    placeholder='Select a date',
                    className='mb-3',
                    style={'width': '300px'}  # Adjust width
                ),
                width=6, className='d-flex justify-content-center'  # Center the column
            )
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
