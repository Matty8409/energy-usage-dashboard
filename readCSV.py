# readCSV.py
import pandas as pd
from dash import Dash, html, dcc, dash_table, dash
from dash.dependencies import Input, Output, State
import plotly.express as px
from dataProcessing import process_uploaded_file, load_initial_csv_data, apply_pulse_ratios

app = Dash()

# Load initial CSV data
initial_df = load_initial_csv_data()

pulse_ratios = {
    'TH-E-01 kWh (kWh) [DELTA] 1': 1,
    'TH-PM-01.TH-G-01 kWh (kWh) [DELTA] 1': 0.1,
    'TH-PM-01.TH-W-01 kWh (kWh) [DELTA] 1': 0.001,
    'TH-PM-01.TH-W-02 kWh (kWh) [DELTA] 1': 0.001
}

initial_df = apply_pulse_ratios(initial_df, pulse_ratios)

energy_meter_options = [
    {'label': 'TH-E-01 kWh (kWh) [DELTA] 1', 'value': 'TH-E-01 kWh (kWh) [DELTA] 1'},
    {'label': 'TH-PM-01.TH-G-01 kWh (kWh) [DELTA] 1', 'value': 'TH-PM-01.TH-G-01 kWh (kWh) [DELTA] 1'},
    {'label': 'TH-PM-01.TH-W-01 kWh (kWh) [DELTA] 1', 'value': 'TH-PM-01.TH-W-01 kWh (kWh) [DELTA] 1'},
    {'label': 'TH-PM-01.TH-W-02 kWh (kWh) [DELTA] 1', 'value': 'TH-PM-01.TH-W-02 kWh (kWh) [DELTA] 1'}
]

app.layout = html.Div([
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
    dcc.Store(id='data-store', data=initial_df.to_dict('records'))
])

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
     Input('data-store', 'data')]
)

def update_output(view_type, selected_energy_type, selected_date, data):
    if data is None:
        return dash.no_update, dash.no_update, dash.no_update

    df_combined = pd.DataFrame(data)
    date_options = [{'label': date, 'value': date} for date in df_combined['Date'].unique()]
    if selected_date is None and date_options:
        selected_date = date_options[0]['value']

    df_filtered = df_combined[df_combined['Date'] == selected_date]

    if view_type == 'table':
        return (dash_table.DataTable(
                    data=df_filtered.to_dict('records'),
                    columns=[{"name": i, "id": i} for i in df_filtered.columns],
                    page_size=len(df_filtered),
                    style_table={'height': '600px', 'overflowY': 'auto'},
                    style_cell={'textAlign': 'center'}
                ),
                date_options,
                selected_date)
    elif view_type == 'graph':
        fig = px.line(df_filtered, x='Time', y=selected_energy_type, color='Date', title=f'Energy Usage Over Time: {selected_energy_type}')
        fig.update_traces(mode='lines+markers')
        return dcc.Graph(figure=fig), date_options, selected_date

if __name__ == '__main__':
    app.run(debug=True)