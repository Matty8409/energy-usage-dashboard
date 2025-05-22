import logging
logging.basicConfig(level=logging.DEBUG)
from dash import no_update

def register_login_callbacks(app, get_dashboard_layout, data):
    @app.callback(
        [Output('theme-wrapper', 'children'),
         Output('url', 'pathname')],
        [Input('login-button', 'n_clicks')],
        [State('username', 'value'),
         State('password', 'value')]
    )
    def update_page_content(n_clicks, username, password):
        if n_clicks:
            response, status_code = login_user(username, password)
            if status_code == 200:  # Login successful
                session['logged_in'] = True
                return get_dashboard_layout(data), '/dashboard'
            else:  # Login failed
                return html.Div("Invalid username or password.", style={'color': 'red'}), no_update

        return get_login_layout(), no_update  # Default to login layout

import dash
from dash import Input, Output, State, html
from flask import session
from app.auth import login_user
from app.layouts.login_layout import get_login_layout

def register_auth_callbacks(app, get_dashboard_layout, data):

    @app.callback(
        Output('theme-wrapper', 'children'),
        [
            Input('login-button', 'n_clicks'),
            Input('register-button', 'n_clicks'),
            Input('go-to-register', 'n_clicks'),
            Input('go-to-login', 'n_clicks')
        ],
        [
            State('username', 'value'),
            State('password', 'value'),
            State('register-username', 'value'),
            State('register-password', 'value')
        ]
    )
    def handle_auth(
        login_clicks, register_clicks, go_to_register_clicks, go_to_login_clicks,
        login_username, login_password,
        reg_username, reg_password
    ):
        triggered = dash.callback_context.triggered_id

        if triggered == 'go-to-login':
            return get_login_layout()

        if triggered == 'login-button':
            if not login_username or not login_password:
                return html.Div([
                    get_login_layout(),
                    html.Div("Username and password are required.", style={'color': 'red'})
                ])
            response, status_code = login_user(login_username, login_password)
            if status_code == 200:
                session['logged_in'] = True
                return get_dashboard_layout(data)
            else:
                return html.Div([
                    get_login_layout(),
                    html.Div(response['error'], style={'color': 'red'})
                ])
        return dash.no_update