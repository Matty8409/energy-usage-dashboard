import pandas as pd
import glob
import os
from dash import Dash, html, dcc, dash_table
from dash.dependencies import Input, Output, State
import plotly.express as px
import base64
import io
import openpyxl

app = Dash()

# Path to CSV files
path = 'CSV_files'
all_files = glob.glob(os.path.join(path, '**', '*.xlsx'), recursive=True)

# Combine data directly into a single DataFrame
combined_data = []
for filename in all_files:
    # Extract date from the file's directory
    date_key = os.path.basename(filename).split('_')[0]

    # Read Excel file into a DataFrame
    df = pd.read_excel(filename, engine='openpyxl')

    # Add a 'Date' column to the DataFrame for easy reference
    df['Date'] = date_key

    # Append the DataFrame to the list
    combined_data.append(df)

# Concatenate all DataFrames into one
df_combined = pd.concat(combined_data, ignore_index=True)

# Sort the DataFrame by 'Date' and 'Time' columns
df_combined = df_combined.sort_values(by=['Date', 'Time'])

# Group by 'Date' and 'Time' and aggregate the data
df_combined = df_combined.groupby(['Date', 'Time'], as_index=False).first()

# Initialize the app layout
app.layout = html.Div([
    html.H1('Energy Usage Dashboard'),
    dcc.RadioItems(
        id='view-type-radio',
        options=[
            {'label': 'Table View', 'value': 'table'},
            {'label': 'Line Graph View', 'value': 'graph'}
        ],
        value='table',  # Default value
        labelStyle={'display': 'inline-block'}
    ),
    dcc.Dropdown(
        id='energy-type-dropdown',
        options=[
            {'label': 'TH-E-01 kWh (kWh) [DELTA] 1', 'value': 'TH-E-01 kWh (kWh) [DELTA] 1'},
            {'label': 'TH-PM-01.TH-G-01 kWh (kWh) [DELTA] 1', 'value': 'TH-PM-01.TH-G-01 kWh (kWh) [DELTA] 1'},
            {'label': 'TH-PM-01.TH-W-01 kWh (kWh) [DELTA] 1', 'value': 'TH-PM-01.TH-W-01 kWh (kWh) [DELTA] 1'},
            {'label': 'TH-PM-01.TH-W-02 kWh (kWh) [DELTA] 1', 'value': 'TH-PM-01.TH-W-02 kWh (kWh) [DELTA] 1'}
        ],
        value='TH-E-01 kWh (kWh) [DELTA] 1'  # Default value
    ),
    html.Div(id='output-container'),
    dcc.Dropdown(id='date-dropdown'),
    dcc.Upload(id='add-XLSX', children=html.Button("Upload XLSX File", className="button"))
])

# Callback to update the display based on the selected view type and energy type
@app.callback(
    [Output('output-container', 'children'),
     Output('date-dropdown', 'options'),
     Output('date-dropdown', 'value')],
    [Input('view-type-radio', 'value'),
     Input('energy-type-dropdown', 'value'),
     Input('add-XLSX', 'contents'),
     Input('date-dropdown', 'value')],
    [State('add-XLSX', 'filename')]
)
def update_output(view_type, selected_energy_type, contents, selected_date, filename):
    global df_combined
    if contents is not None:
        content_type, content_string = contents.split(',')
        decoded = base64.b64decode(content_string)
        df_new = pd.read_excel(io.BytesIO(decoded), engine='openpyxl')

        date_key = os.path.basename(filename).split('_')[0]
        df_new['Date'] = date_key

        df_combined = pd.concat([df_combined, df_new], ignore_index=True)
        df_combined = df_combined.sort_values(by=['Date', 'Time'])
        df_combined = df_combined.groupby(['Date', 'Time'], as_index=False).first()

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