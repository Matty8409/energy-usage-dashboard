import logging
logging.basicConfig(level=logging.DEBUG)
from dash import no_update

def register_login_callbacks(app, get_dashboard_layout, data):
    @app.callback(
        [Output('theme-wrapper', 'children'),  # Update the page content
         Output('url', 'pathname')],          # Update the URL
        [Input('login-button', 'n_clicks'),
         Input('go-to-register', 'n_clicks')],
        [State('username', 'value'), State('password', 'value')]
    )
    def update_page_content(n_clicks, n_register_clicks, username, password):
        if n_register_clicks:
            return get_register_layout(), '/register'  # Redirect to register page

        if n_clicks:
            response, status_code = login_user(username, password)
            if status_code == 200:  # Login successful
                session['logged_in'] = True
                return get_dashboard_layout(data), '/dashboard'  # Redirect to dashboard
            else:  # Login failed
                return html.Div([
                    get_login_layout(),
                    html.Div(response['error'], style={'color': 'red', 'marginTop': '10px'})
                ]), no_update  # Keep the current URL

        return get_login_layout(), no_update  # Default to login layout

import dash
from dash import Input, Output, State, html
from flask import session
from app.auth import login_user, register_user
from app.layouts.register import get_register_layout
from app.layouts.login import get_login_layout

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

        if triggered == 'go-to-register':
            return get_register_layout()

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

        if triggered == 'register-button':
            if not reg_username or not reg_password:
                return html.Div([
                    get_register_layout(),
                    html.Div("Username and password are required.", style={'color': 'red'})
                ])
            response, status_code = register_user(reg_username, reg_password)
            if status_code == 201:
                session['registered'] = True
                return html.Div([
                    get_login_layout(),
                    html.Div("Registration successful. Please log in.", style={'color': 'green'})
                ])
            else:
                return html.Div([
                    get_register_layout(),
                    html.Div(response.get('error', 'Registration failed.'), style={'color': 'red'})
                ])

        return dash.no_update
