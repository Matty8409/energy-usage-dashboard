from dash import html, dcc
from dash.dependencies import Input, Output, State
import pandas as pd
import plotly.graph_objects as go

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

        # Filter or calculate based on the selected energy type
        if energy_type != 'all' and energy_type in df.columns:
            df = df[['Date', 'Time', energy_type]]
        elif energy_type == 'all':
            df['Total Usage'] = df.iloc[:, 2:].sum(axis=1)
            energy_type = 'Total Usage'

        # Calculate the highest day and usage
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

        # Return the statistics and graph as HTML
        return html.Div([
            html.P(f"Highest Day for {energy_type}: {highest_day}"),
            html.P(f"Highest Usage: {highest_usage}"),
            html.P(f"Time of Maximum Usage: {max_time}"),
            dcc.Graph(figure=fig, className='statistics-graph')
        ], className='statistics-written-data')