# app.py
import os
import pandas as pd
import dash_bootstrap_components as dbc
import plotly.express as px
from dash import Dash, html, dcc, dash_table, dash
from dash.dependencies import Input, Output, State
from flask import Flask, session
from app.config import pulse_ratios, energy_meter_options
from app.data_processing import process_uploaded_file, load_initial_csv_data, apply_pulse_ratios
from app.database import init_db
from app.layouts import get_dashboard_layout, get_login_layout
from app.login import register_login_callbacks
from app import routes

# Create a Flask server instance
server = Flask(__name__)

routes.register_routes()

server.config['SECRET_KEY'] = os.urandom(24)

server.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///app.db'
server.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False

# Initialize the database with the Flask server
init_db(server)



app = Dash(
    __name__,
    server=server,
    assets_folder=os.path.join(os.path.dirname(__file__), '../assets')  # Explicitly point to the assets folder
)


app.validation_layout = html.Div([
    get_login_layout(),
    get_dashboard_layout()
])


app.layout = get_login_layout()

register_login_callbacks(app, get_dashboard_layout)


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


import logging


@app.callback(
    [Output('output-container', 'children'),
     Output('date-dropdown', 'options'),
     Output('date-dropdown', 'value'),
     Output('energy-type-dropdown', 'value')],
    [Input('view-type-radio', 'value'),
     Input('energy-type-dropdown', 'value'),
     Input('date-dropdown', 'value'),
     Input('data-store', 'data'),
     Input('theme-store', 'data')],
)
def update_output(view_type, selected_energy_type, selected_date, data, theme):
    if not session.get('logged_in'):  # Check if the user is logged in
        return dash.no_update, dash.no_update, dash.no_update, dash.no_update

    if not data:
        logging.error("Data is empty or None.")
        return dash.no_update, dash.no_update, dash.no_update, dash.no_update

    # Convert data-store to DataFrame
    try:
        df_combined = pd.DataFrame(data)
    except Exception as e:
        logging.error(f"Error converting data to DataFrame: {e}")
        return dash.no_update, dash.no_update, dash.no_update, dash.no_update

    # Ensure required columns exist
    if 'Date' not in df_combined.columns or 'Time' not in df_combined.columns:
        logging.error("Required columns 'Date' or 'Time' are missing.")
        return dash.no_update, dash.no_update, dash.no_update, dash.no_update

    # Generate date options
    try:
        date_options = [
            {'label': 'All Dates', 'value': 'all'},
            {'label': 'All Dates (Average)', 'value': 'average'}
        ] + [{'label': date, 'value': date} for date in df_combined['Date'].unique()]
        if selected_date is None and date_options:
            selected_date = date_options[0]['value']
    except Exception as e:
        logging.error(f"Error generating date options: {e}")
        return dash.no_update, dash.no_update, dash.no_update, dash.no_update

    # Filter or aggregate data by date
    try:
        if selected_date == 'all':
            df_filtered = df_combined
        elif selected_date == 'average':
            numeric_columns = df_combined.select_dtypes(include='number').columns
            if numeric_columns.empty:
                logging.error("No numeric columns available for averaging.")
                return dash.no_update, dash.no_update, dash.no_update, dash.no_update
            df_filtered = df_combined.groupby('Time')[numeric_columns].mean().reset_index()
            df_filtered['Date'] = 'Average'
            columns_order = ['Date'] + [col for col in df_filtered.columns if col != 'Date']
            df_filtered = df_filtered[columns_order]
        else:
            df_filtered = df_combined[df_combined['Date'] == selected_date]
    except Exception as e:
        logging.error(f"Error filtering or aggregating data: {e}")
        return dash.no_update, dash.no_update, dash.no_update, dash.no_update

    # Filter by energy type
    try:
        if selected_energy_type and selected_energy_type != 'all':
            if selected_energy_type in df_filtered.columns:
                df_filtered = df_filtered[['Date', 'Time', selected_energy_type]]
            else:
                logging.error(f"Selected energy type '{selected_energy_type}' not found in columns.")
                return dash.no_update, dash.no_update, dash.no_update, dash.no_update
        else:
            # If 'all' is selected, don't filter down to just one column
            pass

    except Exception as e:
        logging.error(f"Error filtering by energy type: {e}")
        return dash.no_update, dash.no_update, dash.no_update, dash.no_update

    # Render table or graph
    if view_type == 'table':
        try:
            return (dash_table.DataTable(
                data=df_filtered.to_dict('records'),
                columns=[{"name": i, "id": i} for i in df_filtered.columns],
                page_size=len(df_filtered),
                style_table={'height': '600px', 'overflowY': 'auto'}
            ),
                    date_options,
                    selected_date,
                    selected_energy_type)
        except Exception as e:
            logging.error(f"Error creating table view: {e}")
            return dash.no_update, dash.no_update, dash.no_update, dash.no_update

    elif view_type == 'graph':
        try:
            # Melt DataFrame for graphing
            df_melted = df_filtered.melt(
                id_vars=['Time', 'Date'],
                value_vars=[selected_energy_type] if selected_energy_type != 'all' else df_filtered.columns[2:],
                var_name='Energy Type',
                value_name='Usage'
            )

            fig = px.line(
                df_melted,
                x='Time',
                y='Usage',
                color='Energy Type',
                title=f'Energy Usage on {selected_date}' if selected_date not in ['all', 'average'] else 'Energy Usage Over Time',
                labels={'Time': 'Time of Day', 'Usage': 'Energy Usage'}
            )

            return dcc.Graph(figure=fig), date_options, selected_date, selected_energy_type
        except Exception as e:
            logging.error(f"Error creating graph view: {e}")
            return dash.no_update, dash.no_update, dash.no_update, dash.no_update










if __name__ == '__main__':
    app.run(debug=True)

