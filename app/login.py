import logging
from dash import html, Input, Output, State, callback_context
from flask import session
from app.auth import login_user, register_user
from app.pages.dashboard import get_dashboard_layout
from app.pages.login import get_login_layout
from app.pages.register import get_register_layout

logging.basicConfig(level=logging.DEBUG)

def register_login_callbacks(app):
    @app.callback(
        Output('theme-wrapper', 'children'),
        [Input('login-button', 'n_clicks'),
         Input('register-button', 'n_clicks'),
         Input('go-to-register', 'n_clicks'),
         Input('go-to-login', 'n_clicks')],
        [State('username', 'value'),
         State('password', 'value'),
         State('register-username', 'value'),
         State('register-password', 'value')]
    )
    def handle_auth_logic(login_clicks, register_clicks, go_to_register, go_to_login, username, password, reg_username, reg_password):
        ctx = callback_context
        if not ctx.triggered:
            return get_login_layout().children
        button_id = ctx.triggered[0]['prop_id'].split('.')[0]

        if button_id == 'login-button' and login_clicks:
            response, status_code = login_user(username, password)
            if status_code == 200:
                session['logged_in'] = True
                return get_dashboard_layout().children
            else:
                return get_login_layout().children + [
                    html.Div(response['error'], style={'color': 'red', 'marginTop': '10px'})
                ]

        elif button_id == 'register-button' and register_clicks:
            response, status_code = register_user(reg_username, reg_password)
            if status_code == 201:
                return get_login_layout().children + [
                html.Div("Registration Successful! Please log in.", style={'color': 'green', 'textAlign': 'center', 'marginTop': '10px'})
            ]
            else:
                return get_register_layout().children + [
                    html.Div(response['error'], style={'color': 'red', 'marginTop': '10px'})
                ]

        elif button_id == 'go-to-register' and go_to_register:
            return get_register_layout().children

        elif button_id == 'go-to-login' and go_to_login:
            return get_login_layout().children

        return get_login_layout().children