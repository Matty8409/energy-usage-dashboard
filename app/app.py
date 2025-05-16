# app.py
import os
import pandas as pd
import plotly.express as px
import logging
import dash_bootstrap_components as dbc
from dash import Dash, html, dcc, dash_table, dash
from dash.dependencies import Input, Output, State
from flask import Flask, session
from app.config import pulse_ratios, energy_type_mapping, energy_meter_options
from app.data_processing import process_uploaded_file, load_initial_csv_data, apply_pulse_ratios
from app.database import init_db
from app.layouts.dashboard_layout import get_dashboard_layout
from app.layouts.login_layout import get_login_layout
from app.layouts.register_layout import get_register_layout
from app.layouts.statistics_layout import get_statistics_layout
from app.layouts.save_data_collection_layout import get_save_data_collection_layout
from app.data_processing import load_initial_csv_data
from app.layouts.costs_and_carbon_layout import get_costs_and_carbon_layout
from app.login import register_auth_callbacks, register_login_callbacks
from app.register import register_register_callbacks
from app.save_data_collection import register_save_data_callbacks
from app.statistics import register_statistics_callbacks
from app import routes
from app.costs_and_carbon import register_costs_and_carbon_callbacks

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
# Load initial data
initial_df = load_initial_csv_data()
initial_df = apply_pulse_ratios(initial_df, pulse_ratios)

app.layout = html.Div([
    dcc.Location(id='url', refresh=False),
    html.Div(id='page-content'),
    dcc.Store(id='data-store', data=initial_df.to_dict('records'))
])

app.validation_layout = html.Div([  # Ensure that 'url' is part of the validation layout
    dcc.Location(id='url', refresh=False),
    html.Div(id='page-content'),
    dcc.Store(id='data-store', data=initial_df.to_dict('records')),
    get_login_layout(),
    get_dashboard_layout(initial_df),
    get_register_layout(),
    get_statistics_layout(initial_df),
    get_save_data_collection_layout(initial_df, app),
    get_costs_and_carbon_layout(initial_df)
])

@app.callback(
    [Output('data-store', 'data'),
     Output('upload-message', 'children')],
    [Input('add-file', 'contents')],
    [State('add-file', 'filename'),
     State('data-store', 'data')]
)
def upload_files_or_zips(contents_list, filenames, data):
    if contents_list is not None:
        messages = []
        for contents, filename in zip(contents_list, filenames):
            data, message = process_uploaded_file(contents, filename, data)
            messages.append(message)

        updated_df = load_initial_csv_data()
        updated_df = apply_pulse_ratios(updated_df, pulse_ratios)

        # Map long names to simple names for pulse ratios
        from app.config import energy_type_mapping
        pulse_ratios_display = ", ".join(
            [f"{energy_type_mapping.get(k, k)}: {v}" for k, v in pulse_ratios.items()]
        )

        combined_message = " ".join(messages) + f" The following pulse ratios have been applied: {pulse_ratios_display}."
        return updated_df.to_dict('records'), combined_message

    return dash.no_update, ""

@app.callback(Output('page-content', 'children'),
              [Input('url', 'pathname')])
def display_page(pathname):
    # Check if the user is logged in
    if not session.get('logged_in'):
        return get_login_layout()  # Redirect to login layout if not logged in
    # Handle page routing
    if pathname == '/dashboard':
        return get_dashboard_layout(initial_df)
    elif pathname == '/save-data-collection':
        return get_save_data_collection_layout(initial_df, app)
    elif pathname == '/login':
        return get_login_layout()
    elif pathname == '/register':
        return get_register_layout()
    elif pathname == '/statistics':
        return get_statistics_layout(initial_df)
    elif pathname == '/costs-and-carbon':
        return get_costs_and_carbon_layout(initial_df)
    else:
        return get_login_layout()  # Default to login if no matching path

def register_callbacks():
    register_login_callbacks(app, get_dashboard_layout, initial_df)
    register_statistics_callbacks(app)
    register_save_data_callbacks(app)
    register_costs_and_carbon_callbacks(app)

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

    if view_type == 'heatmap':
        try:
            # Default to "Electricity" for heatmap if "all" is selected
            if selected_energy_type == 'all':
                selected_energy_type = 'TH-E-01 kWh (kWh) [DELTA] 1'

            energy_column_for_heatmap = selected_energy_type

            # Get the readable name for display
            readable_energy_type = energy_type_mapping.get(energy_column_for_heatmap, energy_column_for_heatmap)

            if energy_column_for_heatmap in df_filtered.columns:
                df_filtered_heatmap = df_filtered.pivot(index='Time', columns='Date', values=energy_column_for_heatmap)

                fig = px.imshow(
                    df_filtered_heatmap,
                    labels=dict(x="Date", y="Time", color=readable_energy_type),
                    title=f"Heatmap for {readable_energy_type}"
                )
                return dcc.Graph(figure=fig), date_options, selected_date, selected_energy_type
            else:
                logging.error(f"Selected energy type '{selected_energy_type}' not found in the filtered data.")
                return dash.no_update, dash.no_update, dash.no_update, dash.no_update

        except Exception as e:
            logging.error(f"Error creating heatmap view: {e}")
            return dash.no_update, dash.no_update, dash.no_update, dash.no_update


    elif view_type == 'graph':

        try:

            df_melted = df_filtered.melt(

                id_vars=['Time', 'Date'],

                value_vars=(

                    [selected_energy_type]

                    if selected_energy_type != 'all'

                    else df_filtered.columns.difference(['Date', 'Time'])

                ),

                var_name='Energy Type',

                value_name='Usage'

            )

            # Build basic figure

            fig = px.line(

                df_melted,

                x='Time',

                y='Usage',

                color='Energy Type',

                title=(

                    f'Energy Usage on {selected_date}'

                    if selected_date not in ['all', 'average']

                    else 'Energy Usage Over Time'

                ),

                labels={'Time': 'Time of Day', 'Usage': 'Energy Usage'}

            )

            # Update layout
            energy_label_map = {opt['value']: opt['label'] for opt in energy_meter_options}
            # 1) Update the y-axis title to the selected type’s pretty name

            if selected_energy_type != 'all':
                pretty = energy_label_map.get(selected_energy_type, 'Usage')
                fig.update_yaxes(title_text=pretty)

            # 2) Remap each legend entry to its pretty name

            for trace in fig.data:
                raw_name = trace.name  # e.g. 'TH-E-01 kWh (kWh) [DELTA] 1'
                trace.name = energy_label_map.get(raw_name, raw_name)


            return dcc.Graph(figure=fig), date_options, selected_date, selected_energy_type


        except Exception as e:

            logging.error(f"Error creating graph view: {e}")

            return dash.no_update, date_options, selected_date, dash.no_update

@app.callback(
    [Output('toolbar-collapse', 'is_open'),
     Output('toolbar-toggle-button', 'children')],  # Update button text
    [Input('toolbar-toggle-button', 'n_clicks')],
    [State('toolbar-collapse', 'is_open')]
)
def toggle_toolbar(n_clicks, is_open):
    if n_clicks:
        is_open = not is_open  # Toggle the state
    else:
        is_open = is_open  # Keep the current state if no clicks

    # Update button text based on the collapse state
    button_text = "Hide View Selector" if is_open else "Show View Selector"
    return is_open, button_text

if __name__ == '__main__':
    app.run(debug=True)
