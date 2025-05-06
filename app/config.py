pulse_ratios = {
    'TH-E-01 kWh (kWh) [DELTA] 1': 1,
    'TH-PM-01.TH-G-01 kWh (kWh) [DELTA] 1': 0.1,
    'TH-PM-01.TH-W-01 kWh (kWh) [DELTA] 1': 0.001,
    'TH-PM-01.TH-W-02 kWh (kWh) [DELTA] 1': 0.001
}
energy_meter_options = [
    {'label': 'All Energy Types', 'value': 'all'},
    {'label': 'Electricity (kWh)', 'value': 'TH-E-01 kWh (kWh) [DELTA] 1'},
    {'label': 'Gas (kWh)', 'value': 'TH-PM-01.TH-G-01 kWh (kWh) [DELTA] 1'},
    {'label': 'Water 1 (kWh)', 'value': 'TH-PM-01.TH-W-01 kWh (kWh) [DELTA] 1'},
    {'label': 'Water 2 (kWh)', 'value': 'TH-PM-01.TH-W-02 kWh (kWh) [DELTA] 1'}
]
energy_type_mapping = {
    'TH-E-01 kWh (kWh) [DELTA] 1': 'Electricity',
    'TH-PM-01.TH-G-01 kWh (kWh) [DELTA] 1': 'Gas',
    'TH-PM-01.TH-W-01 kWh (kWh) [DELTA] 1': 'Water 1',
    'TH-PM-01.TH-W-02 kWh (kWh) [DELTA] 1': 'Water 2',
    'all': 'All Energy Types'
}