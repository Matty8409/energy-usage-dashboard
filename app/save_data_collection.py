import dash
from dash import Input, Output, State, html
from dash import html
from dash.dependencies import Input, Output

# Define the callback function
import logging


def register_save_data_callbacks(app):
    @app.callback(
        [Output('saved-data-store', 'data'),
         Output('save-data-message', 'children'),
         Output('saved-data-display', 'children')],
        [Input('save-data-button', 'n_clicks')],
        [State('energy-type-dropdown', 'value'),
         State('date-dropdown', 'value'),
         State('saved-data-store', 'data')]
    )
    def save_data(n_clicks, selected_energy_type, selected_date, saved_data):
        logging.debug(
            f"Save Data Triggered: n_clicks={n_clicks}, selected_energy_type={selected_energy_type}, selected_date={selected_date}")

        if n_clicks > 0:
            if selected_energy_type and selected_date:
                new_data = {
                    'energy_type': selected_energy_type,
                    'date': selected_date
                }
                saved_data.append(new_data)
                save_message = "Data saved successfully!"
                saved_data_display = html.Ul([html.Li(f"Energy Type: {data['energy_type']}, Date: {data['date']}")
                                              for data in saved_data])
            else:
                save_message = "Please select both energy type and date."
                saved_data_display = html.Ul([html.Li(f"Energy Type: {data['energy_type']}, Date: {data['date']}")
                                              for data in saved_data])
            return saved_data, save_message, saved_data_display
        return saved_data, "", html.Ul([html.Li(f"Energy Type: {data['energy_type']}, Date: {data['date']}")
                                        for data in saved_data])

