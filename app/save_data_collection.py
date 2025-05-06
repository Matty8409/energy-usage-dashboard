# app/save_data_collection.py
from datetime import datetime
import pandas as pd
import logging
from dash import Input, Output, State, html, dash_table, dcc

def register_save_data_callbacks(app):
    @app.callback(
        [Output('saved-data-store', 'data'),
         Output('save-data-message', 'children'),
         Output('saved-data-display', 'children'),
         Output('filtered-data-preview', 'children')],
        [Input('save-data-button', 'n_clicks')],
        [State('data-store', 'data'),
         State('energy-type-dropdown', 'value'),
         State('date-dropdown', 'value'),
         State('data-input', 'value'),
         State('saved-data-store', 'data')]
    )
    def save_data(n_clicks, data, selected_energy_type, selected_date, user_input, saved_data):
        if saved_data is None:
            saved_data = []

        if not selected_energy_type or not selected_date:
            return saved_data, "Please select both energy type and date.", html.Ul([]), None

        if any(d['energy_type'] == selected_energy_type and d['date'] == selected_date for d in saved_data):
            return saved_data, "This combination has already been saved.", html.Ul([]), None

        if n_clicks > 0:
            if not data:
                return saved_data, "No data available to save.", html.Ul([]), None

            try:
                df = pd.DataFrame(data)
                filtered_df = df[(df['Date'] == selected_date)][['Time', selected_energy_type]]
                table = dash_table.DataTable(
                    columns=[{"name": i, "id": i} for i in filtered_df.columns],
                    data=filtered_df.to_dict('records'),
                    style_table={'overflowX': 'auto'},
                    style_cell={'textAlign': 'left'}
                )

                new_data = {
                    'energy_type': selected_energy_type,
                    'date': selected_date,
                    'input': user_input,
                    'values': filtered_df.to_dict('records'),
                    'datetime': datetime.now().strftime("%Y-%m-%d %H:%M:%S")
                }
                saved_data.append(new_data)

                saved_data_display = html.Ul(
                    [html.Li(f"Energy Type: {data['energy_type']}, Date: {data['date']}") for data in saved_data]
                )
                return saved_data, "Data saved successfully!", saved_data_display, table

            except Exception as e:
                logging.error(f"Error processing data: {e}")
                return saved_data, "An error occurred while saving data.", html.Ul([]), None

        return saved_data, "", html.Ul(
            [html.Li(f"Energy Type: {data['energy_type']}, Date: {data['date']}") for data in saved_data]
        ), None

    @app.callback(
        Output("download-component", "data"),
        Input("download-button", "n_clicks"),
        State("saved-data-store", "data"),
        prevent_initial_call=True
    )
    def download_data(n_clicks, saved_data):
        if not saved_data:
            return None
        flat_records = []
        for entry in saved_data:
            for row in entry['values']:
                row_copy = row.copy()
                row_copy.update({
                    'energy_type': entry['energy_type'],
                    'date': entry['date'],
                    'input': entry.get('input', ''),
                    'saved_at': entry['datetime']
                })
                flat_records.append(row_copy)
        df = pd.DataFrame(flat_records)
        return dcc.send_data_frame(df.to_csv, "saved_data.csv")
