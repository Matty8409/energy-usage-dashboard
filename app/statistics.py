from dash import html, dcc
from dash.dependencies import Input, Output, State
import pandas as pd
import plotly.graph_objects as go

from app.data_processing import get_processed_data


def register_statistics_callbacks(app):
    @app.callback(
        Output('statistics-output', 'children'),
        [Input('statistics-energy-type-dropdown', 'value'),
         Input('data-store', 'data')]
    )
    def calculate_statistics(energy_type, data):
        if not data:
            return "No statistics to display. Please upload data or select an energy type."

        # Convert the data-store to a DataFrame
        df = pd.DataFrame(data)

        # If "all" is selected, calculate stats for each energy type
        if energy_type == 'all':
            energy_columns = df.columns[2:]  # Assuming energy columns start from the 3rd column
            stats_output = []

            for col in energy_columns:
                # Calculate daily usage for the current energy type
                daily_usage = df.groupby('Date')[col].sum()
                highest_day = daily_usage.idxmax()
                highest_usage = daily_usage.max()

                # Filter data for the highest day
                highest_day_data = df[df['Date'] == highest_day]

                # Find the exact time of maximum usage
                max_time_row = highest_day_data.loc[highest_day_data[col].idxmax()]
                max_time = max_time_row['Time']
                max_value = max_time_row[col]

                # Create a line graph for the highest day
                fig = go.Figure()
                fig.add_trace(go.Scatter(
                    x=highest_day_data['Time'],
                    y=highest_day_data[col],
                    mode='lines+markers',
                    name=f'{col} Usage'
                ))

                # Highlight the maximum point
                fig.add_trace(go.Scatter(
                    x=[max_time],
                    y=[max_value],
                    mode='markers',
                    marker=dict(size=10, color='red'),
                    name='Max Usage'
                ))

                fig.update_layout(
                    title=f'{col} Usage on {highest_day}',
                    xaxis_title='Time',
                    yaxis_title=f'{col} Usage',
                    template='plotly_white'
                )

                # Append statistics and graph for the current energy type
                stats_output.append(html.Div([
                    html.P(f"Highest Day for {col}: {highest_day}"),
                    html.P(f"Highest Usage: {highest_usage}"),
                    html.P(f"Time of Maximum Usage: {max_time}"),
                    dcc.Graph(figure=fig, className='statistics-graph')
                ], className='statistics-written-data'))

            return stats_output

        # If a specific energy type is selected
        elif energy_type in df.columns:
            df = df[['Date', 'Time', energy_type]]

            # Calculate daily usage
            daily_usage = df.groupby('Date')[energy_type].sum()
            highest_day = daily_usage.idxmax()
            highest_usage = daily_usage.max()

            # Filter data for the highest day
            highest_day_data = df[df['Date'] == highest_day]

            # Find the exact time of maximum usage
            max_time_row = highest_day_data.loc[highest_day_data[energy_type].idxmax()]
            max_time = max_time_row['Time']
            max_value = max_time_row[energy_type]

            # Create a line graph for the highest day
            fig = go.Figure()
            fig.add_trace(go.Scatter(
                x=highest_day_data['Time'],
                y=highest_day_data[energy_type],
                mode='lines+markers',
                name=f'{energy_type} Usage'
            ))

            # Highlight the maximum point
            fig.add_trace(go.Scatter(
                x=[max_time],
                y=[max_value],
                mode='markers',
                marker=dict(size=10, color='red'),
                name='Max Usage'
            ))

            fig.update_layout(
                title=f'{energy_type} Usage on {highest_day}',
                xaxis_title='Time',
                yaxis_title=f'{energy_type} Usage',
                template='plotly_white'
            )

            # Return the statistics and graph
            return html.Div([
                html.P(f"Highest Day for {energy_type}: {highest_day}"),
                html.P(f"Highest Usage: {highest_usage}"),
                html.P(f"Time of Maximum Usage: {max_time}"),
                dcc.Graph(figure=fig, className='statistics-graph')
            ], className='statistics-written-data')

        return "Invalid energy type selected."

