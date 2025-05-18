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
    'TH-E-01 kWh (kWh) [DELTA] 1': 'Electricity kWh',
    'TH-PM-01.TH-G-01 kWh (kWh) [DELTA] 1': 'Gas m³',
    'TH-PM-01.TH-W-01 kWh (kWh) [DELTA] 1': 'Water 1 m³',
    'TH-PM-01.TH-W-02 kWh (kWh) [DELTA] 1': 'Water 2 m³',
    'all': 'All Energy Types'
}
conversion_factors = {
    'Electricity kWh': {'cost_per_unit': 0.4703, 'carbon_per_unit': 0.2254},  # £0.2/kWh, 0.193 kgCO2/kWh
    'Gas m³': {'cost_per_unit': 0.0989, 'carbon_per_unit': 0.129},        # £0.05/m³, 0.184 kgCO2/m³
    'Water 1 m³': {'cost_per_unit': 3.60, 'carbon_per_unit': 0.344},    # £0.002/m³, 0.344 kgCO2/m³
    'Water 2 m³': {'cost_per_unit': 3.60, 'carbon_per_unit': 0.3389},    # £0.002/m³, 0.344 kgCO2/m³
}