import pytest
from dash import Dash, dcc, html
from app.save_data_collection import register_save_data_callbacks
import pandas as pd
from werkzeug.exceptions import BadRequest

@pytest.fixture
def client():
    # Create a Dash app instance
    app = Dash(__name__)
    register_save_data_callbacks(app)

    # Set a basic layout for the app
    app.layout = html.Div([
        html.Button(id='save-data-button', n_clicks=0),
        dcc.Store(id='data-store'),
        dcc.Store(id='saved-data-store'),
        dcc.Dropdown(id='energy-type-dropdown'),
        dcc.Dropdown(id='date-dropdown'),
        html.Div(id='save-data-message'),
        html.Div(id='saved-data-display')
    ])

    # Configure the app for testing
    app.server.config['TESTING'] = True

    with app.server.test_client() as client:
        yield client

def test_save_data_valid_data(client):
    data = [
        {'Date': '2025-03-27', 'Time': '12:00', 'TH-E-01': 100},
        {'Date': '2025-03-27', 'Time': '13:00', 'TH-E-01': 200}
    ]
    saved_data = []
    selected_energy_type = 'TH-E-01'
    selected_date = '2025-03-27'

    # Simulate a POST request to the callback
    response = client.post('/_dash-update-component', json={
        'outputs': [
            {'id': 'saved-data-store', 'property': 'data'}
        ],
        'inputs': [
            {'id': 'save-data-button', 'property': 'n_clicks', 'value': 1},
            {'id': 'data-store', 'property': 'data', 'value': data},
            {'id': 'energy-type-dropdown', 'property': 'value', 'value': selected_energy_type},
            {'id': 'date-dropdown', 'property': 'value', 'value': selected_date},
            {'id': 'saved-data-store', 'property': 'data', 'value': saved_data}
        ]
    })

    assert response.status_code == 200
    response_data = response.get_json()
    assert response_data['response']['saved-data-store.data'] == [{'energy_type': 'TH-E-01', 'date': '2025-03-27'}]
    assert response_data['response']['save-data-message.children'] == "Data saved successfully!"

def test_save_data_empty(client):
    data = []
    saved_data = []
    selected_energy_type = 'TH-E-01'
    selected_date = '2025-03-27'

    # Simulate a POST request to the callback with no data
    response = client.post('/_dash-update-component', json={
        'outputs': [
            {'id': 'saved-data-store', 'property': 'data'}
        ],
        'inputs': [
            {'id': 'save-data-button', 'property': 'n_clicks', 'value': 1},
            {'id': 'data-store', 'property': 'data', 'value': data},
            {'id': 'energy-type-dropdown', 'property': 'value', 'value': selected_energy_type},
            {'id': 'date-dropdown', 'property': 'value', 'value': selected_date},
            {'id': 'saved-data-store', 'property': 'data', 'value': saved_data}
        ]
    })

    assert response.status_code == 200
    response_data = response.get_json()
    assert response_data['response']['saved-data-store.data'] == saved_data
    assert response_data['response']['save-data-message.children'] == "No data available to save."

def test_save_data_invalid_columns(client):
    data = [
        {'Date': '2025-03-27', 'Time': '12:00', 'InvalidColumn': 100}
    ]
    saved_data = []
    selected_energy_type = 'TH-E-01'
    selected_date = '2025-03-27'

    # Simulate a POST request to the callback with invalid data columns
    response = client.post('/_dash-update-component', json={
        'outputs': [
            {'id': 'saved-data-store', 'property': 'data'}
        ],
        'inputs': [
            {'id': 'save-data-button', 'property': 'n_clicks', 'value': 1},
            {'id': 'data-store', 'property': 'data', 'value': data},
            {'id': 'energy-type-dropdown', 'property': 'value', 'value': selected_energy_type},
            {'id': 'date-dropdown', 'property': 'value', 'value': selected_date},
            {'id': 'saved-data-store', 'property': 'data', 'value': saved_data}
        ],
        'state': []  # If required, include a state field
    })
    assert response.status_code == 200
    response_data = response.get_json()
    assert response_data['response']['saved-data-store.data'] == saved_data
    assert response_data['response']['save-data-message.children'] == "Invalid data format."

def test_save_data_invalid_energy_type(client):
    data = [
        {'Date': '2025-03-27', 'Time': '12:00', 'TH-E-01': 100}
    ]
    saved_data = []
    selected_energy_type = 'TH-E-02'  # Invalid energy type
    selected_date = '2025-03-27'

    # Simulate a POST request to the callback with invalid energy type
    response = client.post('/_dash-update-component', json={
        'outputs': [
            {'id': 'saved-data-store', 'property': 'data'}
        ],
        'inputs': [
            {'id': 'save-data-button', 'property': 'n_clicks', 'value': 1},
            {'id': 'data-store', 'property': 'data', 'value': data},
            {'id': 'energy-type-dropdown', 'property': 'value', 'value': selected_energy_type},
            {'id': 'date-dropdown', 'property': 'value', 'value': selected_date},
            {'id': 'saved-data-store', 'property': 'data', 'value': saved_data}
        ]
    })

    assert response.status_code == 200
    response_data = response.get_json()
    assert response_data['response']['saved-data-store.data'] == saved_data
    assert response_data['response']['save-data-message.children'] == "Energy type 'TH-E-02' is invalid."

def test_save_data_invalid_date(client):
    data = [
        {'Date': '2025-03-27', 'Time': '12:00', 'TH-E-01': 100}
    ]
    saved_data = []
    selected_energy_type = 'TH-E-01'
    selected_date = '2025-03-28'  # Invalid date

    # Simulate a POST request to the callback with an invalid date
    response = client.post('/_dash-update-component', json={
        'outputs': [
            {'id': 'saved-data-store', 'property': 'data'}
        ],
        'inputs': [
            {'id': 'save-data-button', 'property': 'n_clicks', 'value': 1},
            {'id': 'data-store', 'property': 'data', 'value': data},
            {'id': 'energy-type-dropdown', 'property': 'value', 'value': selected_energy_type},
            {'id': 'date-dropdown', 'property': 'value', 'value': selected_date},
            {'id': 'saved-data-store', 'property': 'data', 'value': saved_data}
        ]
    })

    assert response.status_code == 200
    response_data = response.get_json()
    assert response_data['response']['saved-data-store.data'] == saved_data
    assert response_data['response']['save-data-message.children'] == "Date '2025-03-28' is invalid."
