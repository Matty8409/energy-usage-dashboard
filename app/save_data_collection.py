# app/save_data_collection.py
import pandas as pd
import logging
from dash import Input, Output, State, html

def register_save_data_callbacks(app):
    @app.callback(
        [Output('saved-data-store', 'data'),
         Output('save-data-message', 'children'),
         Output('saved-data-display', 'children')],
        [Input('save-data-button', 'n_clicks')],
        [State('data-store', 'data'),
         State('energy-type-dropdown', 'value'),
         State('date-dropdown', 'value'),
         State('saved-data-store', 'data')]
    )
    def save_data(n_clicks, data, selected_energy_type, selected_date, saved_data):
        logging.debug(f"Initial saved_data: {saved_data}")
        if saved_data is None:
            saved_data = []  # Initialize as an empty list if None

        if n_clicks > 0:
            if not data:
                logging.error("Data is empty or None.")
                return saved_data, "No data available to save.", html.Ul([])

            try:
                # Convert data-store to a DataFrame
                df = pd.DataFrame(data)
                logging.debug(f"Data-store converted to DataFrame: {df.head()}")

                if df.empty:
                    logging.error("DataFrame is empty after conversion.")
                    return saved_data, "No valid data available to save.", html.Ul([])

                if 'Date' not in df.columns or 'Time' not in df.columns:
                    logging.error("Required columns 'Date' or 'Time' are missing.")
                    return saved_data, "Invalid data format.", html.Ul([])

                # Validate selected energy type and date
                if selected_energy_type not in df.columns:
                    logging.error(f"Selected energy type '{selected_energy_type}' not found in data.")
                    return saved_data, f"Energy type '{selected_energy_type}' is invalid.", html.Ul([])

                if selected_date not in df['Date'].unique():
                    logging.error(f"Selected date '{selected_date}' not found in data.")
                    return saved_data, f"Date '{selected_date}' is invalid.", html.Ul([])

                # Save the selected data
                new_data = {'energy_type': selected_energy_type, 'date': selected_date}
                saved_data.append(new_data)
                logging.debug(f"Updated saved_data: {saved_data}")

                # Display saved data
                saved_data_display = html.Ul(
                    [html.Li(f"Energy Type: {data['energy_type']}, Date: {data['date']}") for data in saved_data]
                )
                return saved_data, "Data saved successfully!", saved_data_display

            except Exception as e:
                logging.error(f"Error processing data: {e}")
                return saved_data, "An error occurred while saving data.", html.Ul([])

        # Return the current saved data if no new save action
        return saved_data, "", html.Ul(
            [html.Li(f"Energy Type: {data['energy_type']}, Date: {data['date']}") for data in saved_data]
        )
