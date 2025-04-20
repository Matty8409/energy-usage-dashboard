from dash import html, dcc
from app.data_processing import load_initial_csv_data, apply_pulse_ratios
from app.config import pulse_ratios, energy_meter_options
from app.login import get_login_layout


def get_dashboard_layout():
    initial_df = load_initial_csv_data()
    initial_df = apply_pulse_ratios(initial_df, pulse_ratios)

    dashboard_layout = html.Div(id='theme-wrapper', children=[
        html.H1('Energy Usage Dashboard', className='header-title'),
        html.Button('Toggle Toolbar', id='toggle-toolbar-button', className='toolbar-button', n_clicks=0),
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
        dcc.Store(id='data-store', data=initial_df.to_dict('records')),
        html.Div(id='page-content', children=get_login_layout())
    ])
    return dashboard_layout