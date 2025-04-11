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
        value='Energy (kWh)'
    ),
    html.Div(id='output-container'),
    dcc.Dropdown(id='date-dropdown'),
    dcc.Upload(id='add-file', children=html.Button("Upload File or ZIP Folder", className="button"), multiple=True),
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
def upload_files_or_zips(contents_list, filenames, data):
    if contents_list is not None:
        for contents, filename in zip(contents_list, filenames):
            process_uploaded_file(contents, filename, data)

        # Reload the data from the CSV_files directory
        updated_df = load_initial_csv_data()
        updated_df = apply_pulse_ratios(updated_df, pulse_ratios)
        return updated_df.to_dict('records')
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

    # Convert data-store to DataFrame
    df_combined = pd.DataFrame(data)

    # Ensure required columns exist
    if 'Date' not in df_combined.columns or 'Time' not in df_combined.columns:
        return dash.no_update, dash.no_update, dash.no_update

    # Generate date options
    date_options = [{'label': date, 'value': date} for date in df_combined['Date'].unique()]
    if selected_date is None and date_options:
        selected_date = date_options[0]['value']

    # Filter data by selected date
    df_filtered = df_combined[df_combined['Date'] == selected_date]

    if view_type == 'table':
        # Render table
        return (dash_table.DataTable(
            data=df_filtered.to_dict('records'),
            columns=[{"name": i, "id": i} for i in df_filtered.columns],
            page_size=len(df_filtered),
            style_table={'height': '600px', 'overflowY': 'auto'}
        ),
                date_options,
                selected_date)

    elif view_type == 'graph':
        if selected_energy_type == 'all':
            # Plot all energy columns
            energy_columns = [col for col in df_filtered.columns if col in pulse_ratios.keys()]
            if not energy_columns:
                return dash.no_update, dash.no_update, dash.no_update

            # Melt the DataFrame for Plotly
            df_melted = df_filtered.melt(
                id_vars=['Time', 'Date'],
                value_vars=energy_columns,
                var_name='Energy Type',
                value_name='Usage'
            )

            # Render graph
            fig = px.line(
                df_melted,
                x='Time',
                y='Usage',
                color='Energy Type',
                line_group='Date',
                title='Energy Usage Over Time (All Types)',
                labels={'Time': 'Time of Day', 'Usage': 'Energy Usage'}
            )
        else:
            # Ensure the selected energy column exists
            if selected_energy_type not in df_filtered.columns:
                return dash.no_update, dash.no_update, dash.no_update

            # Render graph for a single energy type
            fig = px.line(
                df_filtered,
                x='Time',
                y=selected_energy_type,
                color='Date',
                title=f'Energy Usage Over Time: {selected_energy_type}',
                labels={'Time': 'Time of Day', selected_energy_type: 'Energy Usage'}
            )

        return dcc.Graph(figure=fig), date_options, selected_date

if __name__ == '__main__':
    app.run(debug=True)