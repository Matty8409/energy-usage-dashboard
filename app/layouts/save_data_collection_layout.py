import dash_bootstrap_components as dbc
from dash import html, dcc, dash_table
from app.config import energy_meter_options
from app.layouts.navigation_bar import get_navigation_bar
from app.models import SavedCollection

def get_save_data_collection_layout(data, app):
    with app.server.app_context():  # Ensure the query runs within an app context
        all_rows = SavedCollection.query.order_by(SavedCollection.datetime).all()
        store_data = [{
            'group_name': row.group_name,
            'energy_type': row.energy_type,
            'date': row.date,
            'input': row.input,
            'datetime': row.datetime,
            'values': row.values
        } for row in all_rows]

    save_data_collection_layout = dbc.Container(fluid=True, children=[
        dcc.Store(id='saved-data-store', data=store_data),
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