import pandas as pd
import glob
import os
from dash import Dash, html, dcc, dash_table
from dash.dependencies import Input, Output
import plotly.express as px

# Initialize the Dash app
app = Dash()

# Path to your CSV files
path = 'CSV_files'
all_files = glob.glob(os.path.join(path, '**', '*.xlsx'), recursive=True)

# Combine data directly into a single DataFrame
combined_data = []
for filename in all_files:
    # Extract date from the file's directory
    date_key = os.path.basename(os.path.dirname(filename))

    # Read Excel file into a DataFrame
    df = pd.read_excel(filename)

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
    html.Div(id='output-container')
])

# Callback to update the display based on the selected view type and energy type
@app.callback(
    Output('output-container', 'children'),
    [Input('view-type-radio', 'value'),
     Input('energy-type-dropdown', 'value')]
)
def update_output(view_type, selected_energy_type):
    if view_type == 'table':
        return dash_table.DataTable(
            data=df_combined.to_dict('records'),  # Convert the DataFrame to a dictionary for Dash
            columns=[{"name": i, "id": i} for i in df_combined.columns],
            page_size=50,  # Number of rows per page
            style_table={'height': '300px', 'overflowY': 'auto'},  # Table with scroll
            style_cell={'textAlign': 'center'}  # Center-align text in the cells
        )
    elif view_type == 'graph':
        fig = px.line(df_combined, x='Time', y=selected_energy_type, color='Date', title=f'Energy Usage Over Time: {selected_energy_type}')
        fig.update_traces(mode='lines+markers')  # Ensure lines and markers are visible
        return dcc.Graph(figure=fig)

# Run the app
if __name__ == '__main__':
    app.run(debug=True)











# Example: Accessing data for a specific date
date_to_access = '2025-03-21'
# Filter the DataFrame by the specific date
df_filtered = df_combined[df_combined['Date'] == date_to_access]
# Print the filtered data (optional, for verification)
if not df_filtered.empty:
    print(f"Data for {date_to_access}:")
    print(df_filtered.head)  # Display the first 5 rows for verification
else:
    print(f"No data found for {date_to_access}")