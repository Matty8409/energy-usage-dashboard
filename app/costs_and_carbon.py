from dash import Output, Input, State
import pandas as pd
import logging
from app.config import energy_type_mapping, conversion_factors
from dash import html
from app.data_processing import convert_gas_to_kwh

def register_costs_and_carbon_callbacks(app):
    @app.callback(
        [Output('costs-energy-type-dropdown', 'options'),
         Output('costs-energy-type-dropdown', 'value'),
         Output('costs-start-date-dropdown', 'options'),
         Output('costs-end-date-dropdown', 'options')],
        [Input('data-store', 'data')]
    )
    def update_costs_and_carbon_dropdowns(data):
        if not data:
            logging.error("Data is empty or None in costs_and_carbon.")
            return [], None, [], []

        try:
            df = pd.DataFrame(data)
            df = convert_gas_to_kwh(df)  # Ensure gas is converted

            # Ensure 'Date' column is datetime
            if 'Date' in df.columns:
                df['Date'] = pd.to_datetime(df['Date'], errors='coerce')
                available_dates = df['Date'].dropna().dt.date.unique()
                date_options = [{'label': str(date), 'value': str(date)} for date in sorted(available_dates)]
            else:
                logging.error("'Date' column is missing in the data.")
                date_options = []

            # Energy type dropdown options
            energy_columns = [col for col in df.columns if col not in ['Date', 'Time']]
            energy_options = [{'label': 'All Energy Types', 'value': 'all'}] + [
                {'label': energy_type_mapping.get(col, col), 'value': col} for col in energy_columns
            ]

            default_energy_type = energy_columns[0] if energy_columns else None

            return energy_options, default_energy_type, date_options, date_options

        except Exception as e:
            logging.error(f"Error updating Costs & Carbon dropdowns: {e}")
            return [], None, [], []

    @app.callback(
        Output('costs-and-carbon-output', 'children'),
        [Input('calculate-costs-button', 'n_clicks')],
        [State('data-store', 'data'),
         State('costs-energy-type-dropdown', 'value'),
         State('costs-start-date-dropdown', 'value'),
         State('costs-end-date-dropdown', 'value')]
    )
    def calculate_costs_and_carbon(n_clicks, data, energy_type, start_date, end_date):
        if not n_clicks or not data or not energy_type:
            return "No data to calculate."

        try:
            df = pd.DataFrame(data)
            df = convert_gas_to_kwh(df)  # Ensure gas is converted

            # Ensure 'Date' column is datetime
            df['Date'] = pd.to_datetime(df['Date'], errors='coerce')

            # Filter data by date range
            if start_date and end_date:
                df = df[(df['Date'] >= pd.to_datetime(start_date)) & (df['Date'] <= pd.to_datetime(end_date))]

            # Handle "All" energy types
            if energy_type == 'all':
                total_cost = 0
                total_carbon = 0
                for col in df.columns:
                    if col not in ['Date', 'Time']:
                        readable_energy_type = energy_type_mapping.get(col, col)
                        conversion = conversion_factors.get(readable_energy_type, {})
                        if conversion:
                            cost_per_unit = conversion['cost_per_unit']
                            carbon_per_unit = conversion['carbon_per_unit']
                            total_cost += (df[col] * cost_per_unit).sum()
                            total_carbon += (df[col] * carbon_per_unit).sum()

                return (f"Total Cost: £{total_cost:.2f}, "
                        f"Total Carbon Emissions: {total_carbon:.2f} kgCO2")

            # Filter by specific energy type
            if energy_type in df.columns:
                df = df[['Date', 'Time', energy_type]]
            else:
                return f"Energy type '{energy_type}' not found in data."

            # Apply conversion factors
            readable_energy_type = energy_type_mapping.get(energy_type, energy_type)
            conversion = conversion_factors.get(readable_energy_type, {})
            if not conversion:
                return f"No conversion factors available for '{readable_energy_type}'."

            cost_per_unit = conversion['cost_per_unit']
            carbon_per_unit = conversion['carbon_per_unit']

            df['Cost (£)'] = df[energy_type] * cost_per_unit
            df['Carbon Emissions (kgCO2)'] = df[energy_type] * carbon_per_unit

            # Summarize results
            total_cost = df['Cost (£)'].sum()
            total_carbon = df['Carbon Emissions (kgCO2)'].sum()

            return (f"Total Cost: £{total_cost:.2f}, "
                    f"Total Carbon Emissions: {total_carbon:.2f} kgCO2")

        except Exception as e:
            logging.error(f"Error calculating costs and carbon: {e}")
            return "An error occurred during calculation."

    @app.callback(
        Output('costs-summary-output', 'children'),
        [Input('data-store', 'data')]
    )
    def update_costs_summary(data):
        if not data:
            return "No data available for summary."

        try:
            df = pd.DataFrame(data)
            df = convert_gas_to_kwh(df)  # Ensure gas is converted

            # Ensure 'Date' column is datetime
            df['Date'] = pd.to_datetime(df['Date'], errors='coerce')

            # Initialize summary dictionary
            summary = {}

            # Calculate total costs for each energy type
            for energy_type, readable_name in energy_type_mapping.items():
                if energy_type in df.columns and readable_name != 'All Energy Types':
                    conversion = conversion_factors.get(readable_name, {})
                    if conversion:
                        cost_per_unit = conversion['cost_per_unit']
                        total_cost = (df[energy_type] * cost_per_unit).sum()
                        summary[readable_name] = total_cost

            # Calculate total cost across all energy types
            total_cost = sum(summary.values())

            # Generate summary output
            summary_output = [html.P(f"Total Cost to Date: £{total_cost:.2f}", style={'fontWeight': 'bold'})]
            for energy_type, cost in summary.items():
                summary_output.append(html.P(f"{energy_type}: £{cost:.2f}"))

            return summary_output

        except Exception as e:
            logging.error(f"Error updating costs summary: {e}")
            return "An error occurred while calculating the summary."

    @app.callback(
        Output('carbon-summary-output', 'children'),
        [Input('data-store', 'data')]
    )
    def update_carbon_summary(data):
        if not data:
            return "No data available for summary."

        try:
            df = pd.DataFrame(data)
            df = convert_gas_to_kwh(df)  # Ensure gas is converted

            # Ensure 'Date' column is datetime
            df['Date'] = pd.to_datetime(df['Date'], errors='coerce')

            # Initialize summary dictionary
            summary = {}

            # Calculate total carbon emissions for each energy type
            for energy_type, readable_name in energy_type_mapping.items():
                if energy_type in df.columns and readable_name != 'All Energy Types':
                    conversion = conversion_factors.get(readable_name, {})
                    if conversion:
                        carbon_per_unit = conversion['carbon_per_unit']
                        total_carbon = (df[energy_type] * carbon_per_unit).sum()
                        summary[readable_name] = total_carbon

            # Calculate total carbon emissions across all energy types
            total_carbon = sum(summary.values())

            # Generate summary output
            summary_output = [html.P(f"Total Carbon Emissions to Date: {total_carbon:.2f} kgCO2", style={'fontWeight': 'bold'})]
            for energy_type, carbon in summary.items():
                summary_output.append(html.P(f"{energy_type}: {carbon:.2f} kgCO2"))

            return summary_output

        except Exception as e:
            logging.error(f"Error updating carbon summary: {e}")
            return "An error occurred while calculating the summary."

def get_conversion_factors_info():
    # Generate a list of conversion factor details
    conversion_info = [
        html.Li(
            f"{key}: Cost per unit = £{value['cost_per_unit']}, Carbon per unit = {value['carbon_per_unit']} kgCO2")
        for key, value in conversion_factors.items()
    ]
    return html.Div([
        html.H5("Conversion Factors", className="mt-4"),
        html.Ul(conversion_info, className="text-muted")
    ])
