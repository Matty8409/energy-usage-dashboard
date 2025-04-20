from dash import html, dcc, Input, Output, State
from flask import session
from app.auth import login_user

def get_login_layout():
    return html.Div([
        html.H2("Login", style={'textAlign': 'center'}),
        dcc.Input(id='username', type='text', placeholder='Enter Username', style={'margin': '10px'}),
        dcc.Input(id='password', type='password', placeholder='Enter Password', style={'margin': '10px'}),
        html.Button('Login', id='login-button', n_clicks=0),
        html.Div(id='login-message', style={'color': 'red', 'marginTop': '10px'})
    ])


def register_login_callbacks(app, get_dashboard_layout):
    @app.callback(
        Output('page-content', 'children'),
        [Input('login-button', 'n_clicks')],
        [State('username', 'value'), State('password', 'value')]
    )
    def update_page_content(n_clicks, username, password):
        if n_clicks:
            # Call the login_user function to validate credentials
            response, status_code = login_user(username, password)
            if status_code == 200:  # Login successful
                session['logged_in'] = True
                return get_dashboard_layout()  # Replace with your dashboard layout
            else:  # Login failed
                return html.Div([
                    get_login_layout(),
                    html.Div(response['error'], style={'color': 'red', 'marginTop': '10px'})
                ])
        return get_login_layout()