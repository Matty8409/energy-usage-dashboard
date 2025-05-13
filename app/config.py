pulse_ratios = {
    'TH-E-01 kWh (kWh) [DELTA] 1': 1,
    'TH-PM-01.TH-G-01 kWh (kWh) [DELTA] 1': 0.1,
    'TH-PM-01.TH-W-01 kWh (kWh) [DELTA] 1': 0.001,
    'TH-PM-01.TH-W-02 kWh (kWh) [DELTA] 1': 0.001
}
energy_meter_options = [
    {'label': 'All Energy Types', 'value': 'all'},
    {'label': 'Electricity (kWh)', 'value': 'TH-E-01 kWh (kWh) [DELTA] 1'},
    {'label': 'Gas (m³)', 'value': 'TH-PM-01.TH-G-01 kWh (kWh) [DELTA] 1'},
    {'label': 'Water 1 (m³)', 'value': 'TH-PM-01.TH-W-01 kWh (kWh) [DELTA] 1'},
    {'label': 'Water 2 (m³)', 'value': 'TH-PM-01.TH-W-02 kWh (kWh) [DELTA] 1'}
]
energy_type_mapping = {
    'TH-E-01 kWh (kWh) [DELTA] 1': 'Electricity',
    'TH-PM-01.TH-G-01 kWh (kWh) [DELTA] 1': 'Gas',
    'TH-PM-01.TH-W-01 kWh (kWh) [DELTA] 1': 'Water 1',
    'TH-PM-01.TH-W-02 kWh (kWh) [DELTA] 1': 'Water 2',
    'all': 'All Energy Types'
}
conversion_factors = {
    'Electricity': {'cost_per_unit': 0.15, 'carbon_per_unit': 0.233},  # Example: £0.15/kWh, 0.233 kgCO2/kWh
    'Gas': {'cost_per_unit': 0.05, 'carbon_per_unit': 0.184},         # Example: £0.05/m³, 0.184 kgCO2/m³
    'Water 1': {'cost_per_unit': 0.002, 'carbon_per_unit': 0.001},    # Example: £0.002/m³, 0.001 kgCO2/m³
    'Water 2': {'cost_per_unit': 0.002, 'carbon_per_unit': 0.001}
}