# app.py
import os
import pandas as pd
import plotly.express as px
import logging
import dash_bootstrap_components as dbc
from dash import Dash, html, dcc, dash_table, dash
from dash.dependencies import Input, Output, State
from flask import Flask, session
from app.config import pulse_ratios, energy_type_mapping
from app.data_processing import process_uploaded_file, load_initial_csv_data, apply_pulse_ratios
from app.database import init_db
from app.layouts import get_dashboard_layout, get_login_layout, get_register_layout, get_statistics_layout, get_save_data_collection_layout
from app.login import register_login_callbacks
from app.save_data_collection import register_save_data_callbacks
from app.statistics import register_statistics_callbacks
from app import routes

# Create a Flask server instance
server = Flask(__name__)

routes.register_routes()

server.config['SECRET_KEY'] = os.urandom(24)

DATABASE_URL = os.getenv('DATABASE_URL')

if DATABASE_URL:
    # Heroku's DATABASE_URL sometimes needs slight adjustment for SQLAlchemy
    if DATABASE_URL.startswith("postgres://"):
        DATABASE_URL = DATABASE_URL.replace("postgres://", "postgresql://", 1)

    server.config['SQLALCHEMY_DATABASE_URI'] = DATABASE_URL
else:
    # Local development fallback
    server.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///app.db'

server.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False

# Initialize the database with the Flask server
init_db(server)

app = Dash(
    __name__,
    server=server,
    external_stylesheets=[dbc.themes.FLATLY],
    assets_folder=os.path.join(os.path.dirname(__file__), '../assets')  # Explicitly point to the assets folder
)

app.validation_layout = html.Div([  # Ensure that 'url' is part of the validation layout
    dcc.Location(id='url', refresh=False),
    html.Div(id='page-content'),
    get_login_layout(),
    get_dashboard_layout(),
    get_register_layout(),
    get_statistics_layout(),
    get_save_data_collection_layout()
])

app.layout = html.Div([
    dcc.Location(id='url', refresh=False),  # Ensure that 'url' is in the layout
    html.Div(id='page-content')
])


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

@app.callback(Output('page-content', 'children'),
              [Input('url', 'pathname')])
def display_page(pathname):
    # Check if the user is logged in
    if not session.get('logged_in'):
        return get_login_layout()  # Redirect to login layout if not logged in
    # Handle page routing
    if pathname == '/dashboard':
        return get_dashboard_layout()
    elif pathname == '/save-data-collection':
        return get_save_data_collection_layout()
    elif pathname == '/register':
        return get_register_layout()
    elif pathname == '/statistics':
        return get_statistics_layout()
    else:
        return get_login_layout()  # Default to login if no matching path

def register_callbacks():
    register_login_callbacks(app, get_dashboard_layout)
    register_statistics_callbacks(app)
    register_save_data_callbacks(app)

register_callbacks()

@app.callback(
    [Output('output-container', 'children'),
     Output('date-dropdown', 'options'),
     Output('date-dropdown', 'value'),
     Output('energy-type-dropdown', 'value')],
    [Input('view-type-radio', 'value'),
     Input('energy-type-dropdown', 'value'),
     Input('date-dropdown', 'value'),
     Input('data-store', 'data')],
)
def update_combined(view_type, selected_energy_type, selected_date, data):
    if not session.get('logged_in'):  # Check if the user is logged in
        return dash.no_update, dash.no_update, dash.no_update, dash.no_update

    if not data:
        logging.error("Data is empty or None.")
        return dash.no_update, [], None, dash.no_update

    # Convert data-store to DataFrame
    try:
        df_combined = pd.DataFrame(data)
    except Exception as e:
        logging.error(f"Error converting data to DataFrame: {e}")
        return dash.no_update, [], None, dash.no_update

    # Ensure required columns exist
    if 'Date' not in df_combined.columns or 'Time' not in df_combined.columns:
        logging.error("Required columns 'Date' or 'Time' are missing.")
        return dash.no_update, [], None, dash.no_update

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
        return dash.no_update, [], None, dash.no_update

    # Filter or aggregate data by date
    try:
        if selected_date == 'all':
            df_filtered = df_combined
        elif selected_date == 'average':
            numeric_columns = df_combined.select_dtypes(include='number').columns
            if numeric_columns.empty:
                logging.error("No numeric columns available for averaging.")
                return dash.no_update, date_options, selected_date, dash.no_update
            df_filtered = df_combined.groupby('Time')[numeric_columns].mean().reset_index()
            df_filtered['Date'] = 'Average'
            columns_order = ['Date'] + [col for col in df_filtered.columns if col != 'Date']
            df_filtered = df_filtered[columns_order]
        else:
            df_filtered = df_combined[df_combined['Date'] == selected_date]
    except Exception as e:
        logging.error(f"Error filtering or aggregating data: {e}")
        return dash.no_update, date_options, selected_date, dash.no_update

    # Filter by energy type
    try:
        if selected_energy_type and selected_energy_type != 'all':
            if selected_energy_type in df_filtered.columns:
                df_filtered = df_filtered[['Date', 'Time', selected_energy_type]]
            else:
                logging.error(f"Selected energy type '{selected_energy_type}' not found in columns.")
                return dash.no_update, date_options, selected_date, dash.no_update
            readable_energy_type = energy_type_mapping.get(selected_energy_type, selected_energy_type)
        else:
            readable_energy_type = 'All Energy Types'
    except Exception as e:
        logging.error(f"Error filtering by energy type: {e}")
        return dash.no_update, date_options, selected_date, dash.no_update

    # Render table or graph
    if view_type == 'table':
        try:
            columns = [{"name": energy_type_mapping.get(col, col), "id": col} for col in df_filtered.columns]
            return (
                dash_table.DataTable(
                    data=df_filtered.to_dict('records'),
                    columns=columns,
                    page_size=len(df_filtered),
                    style_table={'maxHeight': '500px', 'overflowY': 'auto', 'border': 'none'},
                    style_cell={'textAlign': 'left', 'padding': '10px'},
                    style_header={'backgroundColor': 'lightgrey', 'fontWeight': 'bold'}
                ),
                date_options,
                selected_date,
                selected_energy_type
            )
        except Exception as e:
            logging.error(f"Error creating table view: {e}")
            return dash.no_update, date_options, selected_date, dash.no_update

    elif view_type == 'graph':
        try:
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
            return dash.no_update, date_options, selected_date, dash.no_update

if __name__ == '__main__':
    app.run(debug=True)
