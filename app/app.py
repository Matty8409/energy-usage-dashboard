# app.py
import pandas as pd
from dash import Dash, html, dcc, dash_table, dash
from dash.dependencies import Input, Output, State
import plotly.express as px
from config import pulse_ratios, energy_meter_options
from data_processing import process_uploaded_file, load_initial_csv_data, apply_pulse_ratios
import dash_bootstrap_components as dbc

LIGHT_THEME = dbc.themes.JOURNAL
DARK_THEME = dbc.themes.CYBORG

app = dash.Dash(external_stylesheets=[LIGHT_THEME])

# Load initial CSV data and apply pulse ratios
initial_df = load_initial_csv_data()
initial_df = apply_pulse_ratios(initial_df, pulse_ratios)

app.layout = html.Div(id='theme-wrapper', children=[
    html.H1('Energy Usage Dashboard'),
    dcc.RadioItems(
        id='view-type-radio',
        options=[
            {'label': 'Table View', 'value': 'table'},
            {'label': 'Line Graph View', 'value': 'graph'}
        ],
        value='table',
        labelStyle={'display': 'inline-block'}
    ),
    dcc.Dropdown(
        id='energy-type-dropdown',
        options=energy_meter_options,
        value='TH-E-01 kWh (kWh) [DELTA] 1'
    ),
    html.Div(id='output-container'),
    dcc.Dropdown(id='date-dropdown'),
    dcc.Upload(id='add-file', children=html.Button("Upload File or ZIP Folder", className="button")),
    dcc.Store(id='data-store', data=initial_df.to_dict('records')),
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

@app.callback(
    Output('theme-store', 'data'),
    Input('theme-toggle', 'value')
)
def store_theme_preference(selected_theme):
    return selected_theme

@app.callback(
    Output('theme-wrapper', 'className'),
    Input('theme-store', 'data')
)
def update_theme_class(theme):
    # Dynamically update the theme for the entire page
    if theme == 'dark':
        return f'{theme}-mode'
    return 'light-mode'

@app.callback(
    Output('data-store', 'data'),
    [Input('add-file', 'contents')],
    [State('add-file', 'filename'),
     State('data-store', 'data')]
)
def upload_file_or_zip(contents, filename, data):
    if contents is not None:
        return process_uploaded_file(contents, filename, data)
    return dash.no_update

@app.callback(
    [Output('output-container', 'children'),
     Output('date-dropdown', 'options'),
     Output('date-dropdown', 'value')],
    [Input('view-type-radio', 'value'),
     Input('energy-type-dropdown', 'value'),
     Input('date-dropdown', 'value'),
     Input('data-store', 'data'),
     Input('theme-store', 'data')],
)
def update_output(view_type, selected_energy_type, selected_date, data, theme):
    if data is None:
        return dash.no_update, dash.no_update, dash.no_update

    df_combined = pd.DataFrame(data)
    date_options = [{'label': date, 'value': date} for date in df_combined['Date'].unique()]
    if selected_date is None and date_options:
        selected_date = date_options[0]['value']

    df_filtered = df_combined[df_combined['Date'] == selected_date]

    if view_type == 'table':
        table_styles = {
            'light': {
                'style_header': {'backgroundColor': '#f0f0f0', 'color': '#000'},
                'style_cell': {'backgroundColor': '#ffffff', 'color': '#000', 'textAlign': 'center'},
                'style_table': {'height': '600px', 'overflowY': 'auto'},
            },
            'dark': {
                'style_header': {'backgroundColor': '#1e1e1e', 'color': '#e0e0e0'},
                'style_cell': {'backgroundColor': '#121212', 'color': '#e0e0e0', 'textAlign': 'center'},
                'style_table': {'height': '600px', 'overflowY': 'auto'},
            }
        }

        styles = table_styles.get(theme, table_styles['light'])

        return (dash_table.DataTable(
            data=df_filtered.to_dict('records'),
            columns=[{"name": i, "id": i} for i in df_filtered.columns],
            page_size=len(df_filtered),
            **styles
        ),
                date_options,
                selected_date)
    elif view_type == 'graph':
        fig = px.line(df_filtered, x='Time', y=selected_energy_type, color='Date', title=f'Energy Usage Over Time: {selected_energy_type}')
        fig.update_traces(mode='lines+markers')
        return dcc.Graph(figure=fig), date_options, selected_date

if __name__ == '__main__':
    app.run(debug=True)