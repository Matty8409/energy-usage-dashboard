# app/save_data_collection.py
from datetime import datetime
import pandas as pd
import logging
from dash import Input, Output, State, html, dash_table, dcc

from app.config import energy_type_mapping


def register_save_data_callbacks(app):
    @app.callback(
        [Output('saved-data-store', 'data'),
         Output('save-data-message', 'children'),
         Output('saved-data-table', 'data')],
        [Input('save-data-button', 'n_clicks')],
        [State('data-store', 'data'),
         State('energy-type-dropdown', 'value'),
         State('date-dropdown', 'value'),
         State('data-input', 'value'),
         State('group-name-input', 'value'),
         State('saved-data-store', 'data')]
    )
    def save_data(n_clicks, data, selected_energy_type, selected_date, user_input, group_name, saved_data):
        if saved_data is None:
            saved_data = []

        if not selected_energy_type or not selected_date:
            return saved_data, "Please select energy type and date.", saved_data

        if n_clicks > 0:
            if not data:
                return saved_data, "No data available to save.", saved_data

            try:
                df = pd.DataFrame(data)
                filtered_df = df[(df['Date'] == selected_date)][['Time', selected_energy_type]]

                new_data = {
                    'energy_type': energy_type_mapping.get(selected_energy_type, selected_energy_type),
                    'date': selected_date,
                    'input': user_input or "N/A",
                    'group_name': group_name or "Ungrouped",
                    'values': filtered_df.to_dict('records'),  # Store actual data
                    'datetime': datetime.now().strftime("%Y-%m-%d %H:%M:%S")
                }
                saved_data.append(new_data)

                # Flatten data for the DataTable
                table_data = [
                    {
                        'energy_type': entry['energy_type'],
                        'date': entry['date'],
                        'input': entry.get('input', ''),
                        'group_name': entry['group_name'],
                        'datetime': entry['datetime'],
                        'summary': f"{len(entry['values'])} records saved"  # Use record count for summary
                    }
                    for entry in saved_data
                ]

                return saved_data, "Data saved successfully!", table_data

            except Exception as e:
                logging.error(f"Error processing data: {e}")
                return saved_data, "An error occurred while saving data.", saved_data

        return saved_data, "", saved_data

    @app.callback(
        Output("download-component", "data"),
        [Input("download-button", "n_clicks")],
        [State("group-selection-dropdown", "value"),
         State("saved-data-store", "data")],
        prevent_initial_call=True
    )
    def download_data(n_clicks, selected_group, saved_data):
        if not saved_data or not selected_group:
            return None

        try:
            # Filter data by selected group
            filtered_data = [entry for entry in saved_data if entry['group_name'] == selected_group]

            if not filtered_data:
                return None

            # Create a DataFrame for the selected group
            df_list = []
            for entry in filtered_data:
                if isinstance(entry['values'], list):
                    df = pd.DataFrame(entry['values'])
                    df['Date'] = entry['date']
                    df['Label'] = entry.get('input', '')
                    df['Saved At'] = entry['datetime']
                    df_list.append(df)

            if not df_list:
                return None

            group_df = pd.concat(df_list, ignore_index=True)

            # Write the Excel file to a BytesIO buffer
            from io import BytesIO
            buffer = BytesIO()
            with pd.ExcelWriter(buffer, engine='openpyxl') as writer:
                group_df.to_excel(writer, sheet_name=selected_group[:31], index=False)
            buffer.seek(0)

            filename = f"{selected_group}.xlsx"
            return dcc.send_bytes(buffer.getvalue(), filename)

        except Exception as e:
            logging.error(f"Error generating download data: {e}")
            return None

    # Update the summary stats callback
    def update_saved_summary_stats(saved_data):
        if not saved_data:
            return "No data saved yet."

        try:
            total_entries = len(saved_data)
            energy_type_counts = pd.DataFrame(saved_data)['energy_type'].map(
                lambda x: energy_type_mapping.get(x, x)
            ).value_counts().to_dict()
            most_recent_date = max(entry['datetime'] for entry in saved_data)

            stats = [
                f"Total Entries: {total_entries}",
                "Energy Type Counts: " + ", ".join(f"{k}: {v}" for k, v in energy_type_counts.items()),
                f"Most Recent Save: {most_recent_date}"
            ]
            return html.Ul([html.Li(stat) for stat in stats])
        except Exception as e:
            logging.error(f"Error updating saved summary stats: {e}")
            return "Error generating statistics."

    @app.callback(
        Output("saved-summary-stats", "children"),
        Input("saved-data-store", "data")
    )
    def update_saved_summary_stats(saved_data):
        if not saved_data:
            return "No data saved yet."

        try:
            total_entries = len(saved_data)
            energy_type_counts = pd.DataFrame(saved_data)['energy_type'].value_counts().to_dict()
            most_recent_date = max(entry['datetime'] for entry in saved_data)

            stats = [
                f"Total Entries: {total_entries}",
                "Energy Type Counts: " + ", ".join(f"{k}: {v}" for k, v in energy_type_counts.items()),
                f"Most Recent Save: {most_recent_date}"
            ]
            return html.Ul([html.Li(stat) for stat in stats])
        except Exception as e:
            logging.error(f"Error updating saved summary stats: {e}")
            return "Error generating statistics."

    @app.callback(
        Output("preview-collapse", "is_open"),
        [Input("toggle-preview-button", "n_clicks")],
        [State("preview-collapse", "is_open")]
    )
    def toggle_preview(n_clicks, is_open):
        if n_clicks:
            return not is_open
        return is_open

    @app.callback(
        [Output("group-selection-dropdown", "options"),
         Output("group-summary", "children")],
        [Input("saved-data-store", "data")]
    )
    def update_group_options(saved_data):
        if not saved_data:
            return [], "No data saved yet."

        try:
            # Get unique group names
            group_names = {entry['group_name'] for entry in saved_data}
            options = [{'label': group, 'value': group} for group in group_names]

            # Generate group summary
            summary = []
            for group in group_names:
                count = sum(1 for entry in saved_data if entry['group_name'] == group)
                summary.append(f"{group}: {count} entries")

            return options, html.Ul([html.Li(item) for item in summary])

        except Exception as e:
            logging.error(f"Error updating group options: {e}")
            return [], "Error generating group summary."


